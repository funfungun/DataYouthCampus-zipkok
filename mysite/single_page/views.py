from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view
from .models import DataEngCsv
from .models import DataEngCsv3
from .serializers import TestDataSerializer
from django.http import JsonResponse
from .forms import AvgCostForm
from django.core import serializers
import json
from django.contrib import messages

def image(request):
    return render(
        request,
        'single_page/image.html'
    )

def index(request):
    return render(
        request,
        'single_page/index.html'
    )

def first(request):
    return render(
        request,
        'single_page/check_and_filter.html'
    )


# 구 / 기격 한페이지에 하는 함수
def check_and_filter(request):
    ms = ['마포구', '서대문구', '종로구']
    latest_list = []
    #######
    #구 먼저 지정
    if request.method == 'POST':  # POST 요청인지 확인
        selected_location = request.POST.getlist('DataEngCsv')

        for location in selected_location:
            if location in ms:
                place_code = ms.index(location)
                latest_list.extend(DataEngCsv3.objects.filter(place_code=place_code))

        latest_list_codes = [item.zipcode for item in latest_list]
        print(latest_list_codes)

    #########
    #월세를 전세로 변환
    title = request.POST.get('title')
    content = request.POST.get('content')
    j = 0
    if title and content:
        mon = int(title)
        monf = int(content)
        r = 0.052  # 전월세변환율(5.2%)
        j = mon + (monf * 12 / r)

    elif title and content is None and request.POST.get('selected_items') == 'year_check':
        mon = int(title)
        monf = 0
        r = 0.052
        j = mon + (monf * 12 / r)

    filtered_one = DataEngCsv3.objects.filter(zipcode__in = latest_list_codes,avg_cost__lte=j)

    #필터로 넘겨주기 위해 json파일 형태로 직렬화
    filter_1_data = [item.zipcode for item in filtered_one]
    filter_1_serialized = json.dumps(filter_1_data)
    request.session['filter_1'] = filter_1_serialized

    print(filter_1_serialized)
    num = len(filter_1_data)
    print(num)

    return render(request, 'single_page/category.html',{'num':num})


#카테고리 선택
def category(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        print("선택된 항목:", selected_items)

        #이전 정보 session을 통해 값 가져옴
        filter_1_serialized = request.session.get('filter_1', [])
        filter_1_data = json.loads(filter_1_serialized)


        # DataEngCsv 모델에서 selected_items에 해당하는 모든 컬럼이 1 이상인 데이터를 추출
        filtered_data = DataEngCsv3.objects.filter(zipcode__in=filter_1_data, **{f"{item}__gte": 1 for item in selected_items})

        filter_2 = {item.zipcode:{'lat':item.lat,'lon':item.lon} for item in filtered_data}
        # 필터로 넘겨주기 위해 json파일 형태로 직렬화
        filter_2_data = [{'zipcode': key, 'lat': value['lat'], 'lon': value['lon']} for key, value in filter_2.items()]
        selected_items_serialized = json.dumps(selected_items)
        request.session['selected_items'] = selected_items_serialized
        print(filter_2.keys())
        num=len(filter_2)

        return render(request, 'single_page/input.html', {'num':num})
        
    else:
        print("POST 요청이 아님")
        return render(request, 'single_page/input.html')
    

#마지막페이지 
def final_page(request):
    if request.method == 'POST':
        
        # session으로 가져오기
        filter_1_serialized = request.session.get('filter_1', [])
        filter_1_data = json.loads(filter_1_serialized)
        selected_items_serialized = request.session.get('selected_items', [])
        selected_items = json.loads(selected_items_serialized)

        # 가져온 정보로 다시 검색
        filtered_data = DataEngCsv3.objects.filter(zipcode__in=filter_1_data,
                                                  **{f"{item}__gte": 1 for item in selected_items})
        # final_recommend에 인풋값으로 쓰기 위해 딕셔너리로 변환
        filter_2 = {item.zipcode: {'lat': item.lat, 'lon': item.lon} for item in filtered_data}

        # 추가정보 받아오기
        destination = str(request.POST.get('destination'))
        limit_time = int(request.POST.get('limit_time'))
        transfer_count = int(request.POST.get('transfer_count'))
        pathtype = int(request.POST.get('pathtype'))
        num = request.POST.get('num')
        print(num)

        # 우편번호 앞에 '0' 넣는 작업
        new_db = {}
        for key,value in filter_2.items():
            new_key = f'0{key}'
            new_db[new_key] = value  
        api_key = "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5"
        zip_code_list = list(new_db.keys())
        print(new_db) # 확인용
        print(zip_code_list) #확인용
        
        #print(zip_code_list[0])
       
        result_2 = final_recommend(new_db,zip_code_list,destination,limit_time, transfer_count, pathtype,api_key)
        
        return render(request,'single_page/result.html',{'result_2' :result_2})
        
    return render(request, 'single_page/input.html')


#######################################################################################################
#################################성민 함수#############################################################
#######################################################################################################


import pandas as pd
import numpy as np
#utf-8기반 URL encoding
from urllib.parse import quote
import requests
import json
#현재시간
#from datetime import datetime
#지도 그리기
import folium


    
    
# 도로명 주소 전체를 입력해서 위도 경도 구하기<함수>
def location_full(addr, api_key):
    # UTF-8 기반 URL encoding
    addr = quote(addr)
    url = f"https://apis.openapi.sk.com/tmap/geo/fullAddrGeo?version=1&fullAddr={addr}"
    headers = {
        "accept": "application/json",
        "appKey": api_key
    }
    response = requests.get(url, headers=headers)
    response = json.loads(response.text)
    lat = float(response['coordinateInfo']['coordinate'][0]['newLat'])
    lon = float(response['coordinateInfo']['coordinate'][0]['newLon'])
    return lat, lon


# 1o개짜리 route 추출
def commute_route(dep_lat, dep_lon, des_lat, des_lon, api_key, count=10, searchDttm='202308090900'):
    url = "https://apis.openapi.sk.com/transit/routes"
    payload = {
        "startX": dep_lon,
        "startY": dep_lat,
        "endX": des_lon,
        "endY": des_lat,
        "lang": 0,
        "format": "json",
        "count": count,
        "searchDttm": searchDttm
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "appKey": api_key
    }
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    result = result['metaData']['plan']['itineraries']
    print(result)
    return result


# limit_time: ~분까지 가능 / transfer_count: 최대(0,1,2,3,4,5,6...) / pathtype: 버스만: [2] ,지하철만: [1] 노상관: [3]
def route_condition_test(route, limit_time, transfer_count, pathtype):
    a = pd.DataFrame(route)
    if pathtype == 3:
        result = a[(a['totalTime'] <= limit_time * 60) & (a['transferCount'] <= transfer_count)]
    else:
        result = a[(a['totalTime'] <= limit_time * 60) & (a['transferCount'] <= transfer_count) & (a['pathType'] == pathtype)]
    return result


# 지도 그리기 준비1
def Path_list(path):
    result = dict()
    for i in range(len(path)):
        a = path[i]
        result[f'{i}'] = {}
        route = []
        start_point = (a['start']['lat'], a['start']['lon'])
        route.append(start_point)
        if i in (0, len(path) - 1):
            b = a['steps']
            for j in range(len(b)):
                c = b[j]['linestring'].split(' ')
                for k in range(len(c)):
                    lon, lat = c[k].split(',')
                    route.append((float(lat), float(lon)))
        else:
            b = a['passShape']['linestring'].split(' ')
            for k in range(len(b)):
                lon, lat = b[k].split(',')
                route.append((float(lat), float(lon)))
        end_point = (a['end']['lat'], a['end']['lon'])
        route.append(end_point)
        result[f'{i}']['time'] = a['sectionTime']
        result[f'{i}']['type'] = a['mode'].lower()
        result[f'{i}']['path'] = route
    return result


# 지도 그리기
def draw_map(path_list, lgd_txt="<span style='color:{col};'>{txt}</span>"):
    start_point = path_list['0']['path'][0]
    end_point = path_list[f'{len(path_list) - 1}']['path'][-1]
    center = (start_point[0] + end_point[0]) / 2, (start_point[1] + end_point[1]) / 2
    color = {'walk': '#CCCCCC', 'bus': '#53B332', 'subway': '#0052A4', 'transfer': '#CCCCCC'}
    my_map = folium.Map(location=center, zoom_start=14, tiles=None)
    fg_start_point = folium.FeatureGroup(name=lgd_txt.format(col='green', txt="출발"))
    start_marker = folium.Marker(location=start_point, icon=folium.Icon(color="green", icon="play", prefix="fa"))
    fg_end_point = folium.FeatureGroup(name=lgd_txt.format(col='red', txt="도착"))
    end_marker = folium.Marker(location=end_point, icon=folium.Icon(color="red", icon="stop", prefix="fa"))
    circle_layer = folium.Circle(location=start_point, radius=500, color=None, fill_color='#CE21FA', opacity=0.3, fill=True)
    start_marker.add_to(fg_start_point)
    end_marker.add_to(fg_end_point)
    circle_layer.add_to(fg_start_point)
    fg_start_point.add_to(my_map)
    for i in range(len(path_list)):
        fg_route = folium.FeatureGroup(name=lgd_txt.format(col=color[path_list[f'{i}']['type']], txt=f"{path_list[f'{i}']['type']}{i+1}"))
        route_1 = folium.PolyLine(locations=path_list[f'{i}']['path'], color='#696969', weight=10)
        route_2 = folium.PolyLine(locations=path_list[f'{i}']['path'], color=color[path_list[f'{i}']['type']], weight=6)
        route_1.add_to(fg_route)
        route_2.add_to(fg_route)
        fg_route.add_to(my_map)
    fg_end_point.add_to(my_map)
    return my_map


# reverse_geocoding
def reverse_geo_coding(lat, lon, api_key):
    url = f"https://apis.openapi.sk.com/tmap/geo/reversegeocoding?version=1&lat={lat}&lon={lon}&coordType=WGS84GEO&addressType=A10&newAddressExtend=Y"

    headers = {
        "accept": "application/json",
        "appKey": api_key
    }
    response = requests.get(url, headers=headers)
    result = json.loads(response.text)
    result = result['addressInfo']
    #'주소 추출'/'서울특별시' / '행정동' / '법정동' 추출
    juso,city_gu, admin_dong, legal_dong = result['fullAddress'].split(',')[2],result['city_do'] + ' ' + result['gu_gun'], result['adminDong'], result['legalDong']
    return juso,city_gu, admin_dong, legal_dong

#걷는거 추가할까?
def walk_route(dep_lat,dep_lon,des_lat,des_lon,destination,api_key):
    juso=reverse_geo_coding(dep_lat,dep_lon,api_key)[0]
    url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&callback=function"

    payload = {
        "startX": dep_lon,
        "startY": dep_lat,
        "angle": 20,
        "speed": 5,
        "endPoiId": "10001",
        "endX": des_lon,
        "endY": des_lat,
        "reqCoordType": "WGS84GEO",
        "startName": f"{quote(juso)}",
        "endName": f"{quote(destination)}",
        "searchOption": "0",
        "resCoordType": "WGS84GEO",
        "sort": "index"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "appKey": api_key
    }
    response = requests.post(url, json=payload, headers=headers)
    response=json.loads(response.text)
    response=pd.DataFrame(response['features'])
    result=dict()
    result['0']=dict()
    result['0']['totalTime']=response['properties'][0]['totalTime']
    result['0']['type']='walk'
    result['0']['pathType']='walk'
    response=response['geometry']
    b=list()
    for i in range(len(response)):
        if response[i]['type']=='LineString':
            c=response[i]['coordinates']
            for i in range(len(c)):
                d=c[i]
                e=(d[1],d[0])
                b.append(e)
    result['0']['path']=b
    return result

# 최종 함수
def final_recommend(dataset, zip_code_list, destination, limit_time, transfer_count, pathtype, api_key):
    result = dict()
    for i in range(len(zip_code_list)):
        
        dep_lat, dep_lon = dataset[zip_code_list[i]]['lat'], dataset[zip_code_list[i]]['lon']
        des_lat, des_lon = location_full(destination, api_key)
        print(i,des_lat,des_lon)
        if pathtype == 0 :
            a=walk_route(dep_lat,dep_lon,des_lat,des_lon,destination,api_key)
            c=walk_route(dep_lat,dep_lon,des_lat,des_lon,destination,api_key)
            c['totalTime']=c['0']['totalTime']
            c['pathType']=c['0']['pathType']
            if (c['0']['totalTime']//60) <= limit_time :
                result[zip_code_list[i]] = dict()
                result[zip_code_list[i]]['walk_1'] = c['0']['totalTime']//60
                result[zip_code_list[i]]['totalTime'] = c['totalTime'] // 60
                my_map= draw_map(a)
            else :
                continue
        else :
            try:
                a = commute_route(dep_lat, dep_lon, des_lat, des_lon, api_key)
            except KeyError:
                continue
            b = route_condition_test(a, limit_time, transfer_count, pathtype)
            if b.shape[0] > 0:
                result[zip_code_list[i]] = dict()
                c = b[b['totalTime'] == b['totalTime'].min()].iloc[0, :]
                path_list = Path_list(c['legs'])
                e = 0
                result[zip_code_list[i]]['totalTime'] = c['totalTime'] // 60
                for j in range(len(path_list)):
                    d = path_list[f'{j}']['type'] + f'{j+1}'
                    if j < len(path_list) - 1:
                        result[zip_code_list[i]][d] = path_list[f'{j}']['time'] // 60
                        e += result[zip_code_list[i]][d]
                    else:
                        result[zip_code_list[i]][d] = result[zip_code_list[i]]['totalTime'] - e
                my_map = draw_map(path_list)
            else :
                continue
        folium.TileLayer('OpenStreetMap', name=f'{zip_code_list[i]}', min_zoom=12, max_zoom=16, control=True, opacity=0.7).add_to(my_map)
        folium.map.LayerControl('topleft', collapsed=False).add_to(my_map)
        city_gu, admin_dong, legal_dong = reverse_geo_coding(dep_lat, dep_lon, api_key)[1:]       
        result[zip_code_list[i]]['city_gu'] = city_gu
        result[zip_code_list[i]]['admin_dong'] = admin_dong
        result[zip_code_list[i]]['legal_dong'] = legal_dong
        
        result[zip_code_list[i]]['pathType'] = c['pathType']
        result[zip_code_list[i]]['map'] = my_map._repr_html_()
    try:
        sorted_result = sorted(result.items(), key=lambda item: item[1]['totalTime'])
    except KeyError:
        sorted_result=dict()
    result = dict(sorted_result)
    print(result)
    return result
