from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view
from .models import DataEngCsv
from .serializers import TestDataSerializer
from django.http import JsonResponse
from .forms import AvgCostForm

##

##
information = []

def index(request):
    return render(
        request,
        'single_page/index.html'
    )

def first(request):
    return render(
        request,
        'single_page/autonomous.html'
    )

# def autonomous(request):
#     ms = ['마포구', '서대문구', '종로구']
#     latest_list = []

#     if request.method == 'POST':
#         selected_location = request.POST.getlist('DataEngCsv')

#         for location in selected_location:
#             if location == '마포구':
#                 latest_list.extend(DataEngCsv.objects.filter(place_code=0))
#             elif location == '서대문구':
#                 latest_list.extend(DataEngCsv.objects.filter(place_code=1))
#             elif location == '종로구':
#                 latest_list.extend(DataEngCsv.objects.filter(place_code=2))
#             elif location == '마포구'and location == '서대문구' :
#                 latest_list.extend(DataEngCsv.objects.filter(place_code=[0,1]))
#             elif location == '마포구'and location == '종로구' :
#                 latest_list.extend(DataEngCsv.objects.filter(place_code=[0,2]))
#             elif location == '서대문구'and location == '종로구' :
#                 latest_list.extend(DataEngCsv.objects.filter(place_code=[1,2]))
#             elif location == '마포구' and location == '서대문구'and location == '종로구' :
#                 latest_list.extend(DataEngCsv.objects.filter(place_code=[0,1,2]))

#         global information
#         information = latest_list

#         num = len(latest_list)
#         print(information[0])
#         # request.session['latest_list'] = latest_list
#         return render(request, "single_page/price.html", {'num' : num})

#     else:
#         print("POST 요청이 아님")

def autonomous(request):

    ms = ['마포구', '서대문구', '종로구']
    latest_list = []

    if request.method == 'POST':  # POST 요청인지 확인
        selected_location = request.POST.getlist('DataEngCsv')

        for location in selected_location:
            if location in ms:
                place_code = ms.index(location)
                latest_list.extend(DataEngCsv.objects.filter(place_code=place_code))
        
        global information
        information = latest_list

        num = len(latest_list)
        return render(request, "single_page/price.html", {'num': num})

    else:  # POST 요청이 아닐 때
        print("POST 요청이 아님")
        return render(request, "single_page/autonomous.html")


def price(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    j = 0

    if type(title) == str and type(content) == str:
        mon = int(title)
        monf = int(content)
        r = 0.052  # 전월세변환율(5.2%)
        j = mon + (monf * 12 / r)
        print(j)

        filtered_one = DataEngCsv.objects.filter(avg_cost__lte = j)

        global information
        information = [item for item in filtered_one if item in information]
        print(information)
        num = len(information)
        return render(request, 'single_page/category.html', {'num': num})

    else:
        print("POST 요청이 아님")
        return render(request, 'single_page/category.html')

# 구 / 기격 한페이지에 하는 함수 ( url 연결은 아직 안 함 )
def check_and_filter(request):
    ms = ['마포구', '서대문구', '종로구']
    latest_list = []

    if request.method == 'POST':
        selected_location = request.POST.getlist('DataEngCsv')

        for location in selected_location:
            if location == '마포구':
                latest_list.extend(DataEngCsv.objects.filter(place_code=0))
            elif location == '서대문구':
                latest_list.extend(DataEngCsv.objects.filter(place_code=1))
            elif location == '종로구':
                latest_list.extend(DataEngCsv.objects.filter(place_code=2))
            elif location == '마포구'and location == '서대문구' :
                latest_list.extend(DataEngCsv.objects.filter(place_code=[0,1]))
            elif location == '마포구'and location == '종로구' :
                latest_list.extend(DataEngCsv.objects.filter(place_code=[0,2]))
            elif location == '서대문구'and location == '종로구' :
                latest_list.extend(DataEngCsv.objects.filter(place_code=[1,2]))
            elif location == '마포구' and location == '서대문구'and location == '종로구' :
                latest_list.extend(DataEngCsv.objects.filter(place_code=[0,1,2]))

        
        request.session['latest_list'] = [item.zipcode for item in latest_list]
        
    title = request.POST.get('title')
    content = request.POST.get('content')
    j = 0
    if title and content:
        mon = int(title)
        monf = int(content)
        r = 0.052  # 전월세변환율(5.2%)
        j = mon + (monf * 12 / r)
    
    latest_list_codes = request.session.get('latest_list',[])
    print(latest_list_codes)
    len(latest_list_codes)
    print(latest_list_codes[0])
    print(j)
    filtered_one = DataEngCsv.objects.filter(zipcode__in = latest_list_codes,avg_cost__lte=j)
    
    global information
    information = [item for item in filtered_one ]
    print(information)
    num = len(information)


    print(filtered_one)
    len(filtered_one)
    return render(request, 'single_page/category.html',{'num':num,'filtered_one':filtered_one})


#카테고리 선택
def category(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        print("선택된 항목:", selected_items)

        # DataEngCsv 모델에서 selected_items에 해당하는 모든 컬럼이 1 이상인 데이터를 추출
        filtered_data = DataEngCsv.objects.filter(**{f"{item}__gte": 1 for item in selected_items})

        
        global information
        #information = [item for item in filtered_data if item in information]
        information = {item.zipcode:{'lat':item.lat,'lon':item.lon} for item in filtered_data if item in information}
        print(information.keys())
        num=len(information)
        return render(request, 'single_page/input.html',{'num':num})

    else:
        print("POST 요청이 아님")
        return render(request, 'single_page/input.html')
#마지막페이지 
def final_page(request):
    if request.method == 'POST':
        destination = str(request.POST.get('destination'))
        limit_time = int(request.POST.get('limit_time'))
        transfer_count = int(request.POST.get('transfer_count'))
        pathtype = int(request.POST.get('pathtype'))

        
        global information
        # final_recommend에 인풋값으로 쓰기 위해 딕셔너리로 변환
        information = {key:{'lat':value['lat'],'lon':value['lon']} for key, value in information.items()}
        # 우편번호 앞에 '0' 넣는 작업
        new_db = {}
        for key,value in information.items():
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

def qq(request):
    return render(
        request,
        'single_page/qq.html'
    )




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
    city_gu, admin_dong, legal_dong = result['city_do'] + ' ' + result['gu_gun'], result['adminDong'], result['legalDong']
    return city_gu, admin_dong, legal_dong


# 최종 함수
def final_recommend(dataset, zip_code_list, destination, limit_time, transfer_count, pathtype, api_key):
    result = dict()
    for i in range(len(zip_code_list)):
        dep_lat, dep_lon = dataset[zip_code_list[i]]['lat'], dataset[zip_code_list[i]]['lon']
        des_lat, des_lon = location_full(destination, api_key)
        print(i,des_lat,des_lon)
        a = commute_route(dep_lat, dep_lon, des_lat, des_lon, api_key)
        print(a)
        b = route_condition_test(a, limit_time, transfer_count, pathtype)
        if b.shape[0] > 0:
            c = b[b['totalTime'] == b['totalTime'].min()].iloc[0, :]
            path_list = Path_list(c['legs'])
            my_map = draw_map(path_list)
            folium.TileLayer('OpenStreetMap', name=f'{zip_code_list[i]}', min_zoom=12, max_zoom=16, control=True, opacity=0.7).add_to(my_map)
            folium.map.LayerControl('topleft', collapsed=False).add_to(my_map)
            city_gu, admin_dong, legal_dong = reverse_geo_coding(dep_lat, dep_lon, api_key)
            result[zip_code_list[i]] = dict()
            result[zip_code_list[i]]['city_gu'] = city_gu
            result[zip_code_list[i]]['admin_dong'] = admin_dong
            result[zip_code_list[i]]['legal_dong'] = legal_dong
            result[zip_code_list[i]]['totalTime'] = c['totalTime'] // 60
            e = 0
            for j in range(len(path_list)):
                d = path_list[f'{j}']['type'] + f'{j+1}'
                if j < len(path_list) - 1:
                    result[zip_code_list[i]][d] = path_list[f'{j}']['time'] // 60
                    e += result[zip_code_list[i]][d]
                else:
                    result[zip_code_list[i]][d] = result[zip_code_list[i]]['totalTime'] - e
            result[zip_code_list[i]]['pathType'] = c['pathType']
            result[zip_code_list[i]]['map'] = my_map
        else:
            result[zip_code_list[i]] = list()
    print(result)
    return result
    