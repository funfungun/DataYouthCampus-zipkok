from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view
from .models import DataEngCsv3
from .models import DataEngCsv3
from .serializers import TestDataSerializer
from django.http import JsonResponse
from .forms import AvgCostForm
from django.core import serializers
import json
from django.contrib import messages
from .models import PlzCategory
from collections import defaultdict

def o3091(request):
    return render(
        request,
        'single_page/03091.html'
    )

def o3106(request):
    return render(
        request,
        'single_page/03106.html'
    )

def o3633(request):
    return render(
        request,
        'single_page/03633.html'
    )

def o3757(request):
    return render(
        request,
        'single_page/03757.html'
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


# 구 / 가격 한페이지에 하는 함수
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

    # 마지막 페이지에 보증금/월세, 전세 정보를 보여주기 위해 session에 저장
    request.session['mon'] = mon
    request.session['monf'] = monf

    num = len(filter_1_data) # 필터링 후 남은 우편번호 개수
    

    return render(request, 'single_page/category.html',{'num':num,'mon':mon,'monf':monf})


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
        
        selected_items_serialized = json.dumps(selected_items)
        request.session['selected_items'] = selected_items_serialized
        
        num=len(filter_2) # 필터링 후 남은 개수

        mon = request.session['mon']
        monf = request.session['monf']

        return render(request, 'single_page/input.html', {'num':num,'mon':mon,'monf':monf})
        
    else:
        print("POST 요청이 아님")
        return render(request, 'single_page/input.html')
    

#마지막페이지 
def final_page(request):
    if request.method == 'POST':
        
        # session으로 가져오기
        mon = request.session['mon']
        monf = request.session['monf']
        filter_1_serialized = request.session.get('filter_1', [])
        filter_1_data = json.loads(filter_1_serialized)
        selected_items_serialized = request.session.get('selected_items', [])
        selected_items = json.loads(selected_items_serialized)
        print(selected_items)
        # 가져온 정보로 다시 검색
        filtered_data = DataEngCsv3.objects.filter(zipcode__in=filter_1_data,
                                                  **{f"{item}__gte": 1 for item in selected_items})
               
        filter_2 = {}
        for item in filtered_data:
            data_dict = {'lat':item.lat, 'lon':item.lon, 'avg_cost':item.avg_cost}

            #선택한 카테고리의 리스트를 딕셔너리에 추가
            for field in selected_items:
                data_dict[field] = getattr(item, field)
            
            filter_2[item.zipcode] = data_dict
        print(filter_2.keys())
        # final_recommend 함수에 들어가는 인풋 데이터 우편번호 앞에 '0' 넣는 작업
        new_db = {}
        for key,value in filter_2.items():
            new_key = f'0{key}'
            new_db[new_key] = value  

        # 카테고리 시설 정보 불러오기 위한 작업
        # 우편번호별 카테고리 상세 좌표가 들어있는 PlzCategory DB를 필터링
        fac_data = PlzCategory.objects.filter(zipcode__in = filtered_data)
        # PlzCategory의 모든 필드값들을 딕셔너리에 추가하는 작업
        fields = ['bus_stop', 'art', 'bike', 'gym', 'chatolic', 'hospital', 'perform_place', 'park', 'theater', 'subway', 'animal_hospital', 'beauty_care', 'coin_karaoke', 'liberary', 'church', 'big_mart', 'gonggogng_gym', 'cafe', 'police_office', 'daiso', 'bar', 'shopping_center', 'super_market', 'pharmacy', 'banchan', 'convience_store', 'bank', 'coin_wash_room', 'yoga', 'cross_fit', 'atm', 'food_store', 'post_office', 'pc_room', 'piilates', 'citizen_center', 'temple','bus_stop_info', 'art_info', 'bike_info', 'gym_info', 'chatolic_info', 'hospital_info', 'perform_place_info', 'park_info', 'theater_info', 'subway_info', 'animal_hospital_info', 'beauty_care_info', 'coin_karaoke_info', 'liberary_info', 'church_info', 'big_mart_info', 'gonggogng_gym_info', 'cafe_info', 'police_office_info', 'daiso_info', 'bar_info', 'shopping_center_info', 'super_market_info', 'pharmacy_info', 'banchan_info', 'convience_store_info', 'bank_info', 'coin_wash_room_info', 'yoga_info', 'cross_fit_info', 'atm_info', 'food_store_info', 'post_office_info', 'pc_room_info', 'piilates_info', 'citizen_center_info', 'temple_info']
        result_dict = {}
        for item in fac_data:
            result_dict[item.zipcode] = {'lat':item.lat,'lon':item.lon,}
            for field_name in fields:
                result_dict[item.zipcode][field_name] = getattr(item,field_name)
        # facility_map 함수에 들어갈 데이터 우편번호에 0 넣는 작업
        new_fac = {}
        for key, value in result_dict.items():
            new_key_2 = f'0{key}'
            new_fac[new_key_2] = value
        
        #print(len(new_fac)) # 확인용

        # 사용자에게 추가정보 받아오기
        destination = str(request.POST.get('destination')) # 목적지
        limit_time = int(request.POST.get('limit_time')) # 원하는 이동시간
        transfer_count = int(request.POST.get('transfer_count')) # 원하는 환승횟수
        pathtype = int(request.POST.get('pathtype')) # 원하는 이동수단
        num = request.POST.get('num') # 필터링 후 남은 우편번호 개수 확인용
        print(num)
        # api키 입력
        api_key = "e8wHh2tya84M88aReEpXCa5XTQf3xgo01aZG39k5" 
        
        zip_code_list = list(new_db.keys()) # final_recommend에 들어가는 우편번호의 리스트
        
        # result_2 : final_recommend 함수를 통해 해당 우편번호에서 목적지까지의 경로 및 우편번호의 대략적인 정보 제공       
        result_2 = final_recommend(new_db,zip_code_list,destination,limit_time, transfer_count, pathtype,api_key)
        # result_3 : facility_map 함수를 통해 해당 우편번호 500m 반경 위치하는 카테고리들의 정보를 지도로 제공
        result_3 = facility_map(new_fac,selected_items)
        
        return render(request,'single_page/result.html',{'result_2' :result_2,'mon':mon,'monf':monf,'result_3':result_3})
        
    return render(request, 'single_page/input.html')
    


# 우편번호에서 목적지까지의 이동 경로 제공하는 함수 모음

import numpy as np
#utf-8기반 URL encoding
from urllib.parse import quote
import requests
import json
#현재시간
#from datetime import datetime
#지도 그리기
import folium
import pandas as pd

    
    
# 도로명 주소 전체를 입력해서 위도 경도 구하기<함수>
def location_full(addr, api_key):
    # UTF-8 기반 URL encoding
    addr = quote(addr) # 주소 입력
    url = f"https://apis.openapi.sk.com/tmap/geo/fullAddrGeo?version=1&fullAddr={addr}"
    headers = {
        "accept": "application/json",
        "appKey": 'OWYU6Tu4YP2Xt2Goijjb96P6ZdMoMJeS1OJJuX5v'
    }
    response = requests.get(url, headers=headers)
    response = json.loads(response.text)
    # 위도, 경도 추출
    lat = float(response['coordinateInfo']['coordinate'][0]['newLat'])
    lon = float(response['coordinateInfo']['coordinate'][0]['newLon'])
    return lat, lon


# 1o개짜리 route 추출
def commute_route(dep_lat, dep_lon, des_lat, des_lon, api_key, count=10, searchDttm='202308090900'):
    url = "https://apis.openapi.sk.com/transit/routes"
    payload = {
        "startX": dep_lon, # 출발지 경도
        "startY": dep_lat, # 출발지 위도
        "endX": des_lon, # 도착지 경도
        "endY": des_lat, # 도착지 위도
        "lang": 0,
        "format": "json",
        "count": count, # 뽑고 싶은 경로 개수
        "searchDttm": searchDttm # 검색일자
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "appKey": api_key
    }
    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    result = result['metaData']['plan']['itineraries'] # 경로에 관한 정보 반환
    
    return result

# limit_time: ~분까지 가능 / transfer_count: 최대로 환승 가능한 횟수 (0,1,2,3,4,5,6...) 
# pathtype(교통수단): [2]:버스 , [1]:지하철, [3]:지하철+버스

def route_condition_test(route, limit_time, transfer_count, pathtype):
    a = pd.DataFrame(route)
    if pathtype == 3:
        # 최대시간, 환승횟수, 이동수단 조건 만족하는 결과 반환
        result = a[(a['totalTime'] <= limit_time * 60) & (a['transferCount'] <= transfer_count)]
    else: # 버스만, 혹은 지하철만 이용하고 싶은 경우
        result = a[(a['totalTime'] <= limit_time * 60) & (a['transferCount'] <= transfer_count) & (a['pathType'] == pathtype)]
    return result


# 지도 그리기 준비 : 이동수단별(걷기, 지하철, 버스) 출발지점, 도착지점 좌표 및 이동 경로 좌표의 집합들을 구하는 함수
def Path_list(path):
    result = dict()
    for i in range(len(path)): # 경로 개수만큼
        a = path[i]
        result[f'{i}'] = {}
        route = []
        start_point = (a['start']['lat'], a['start']['lon']) # 이동수단별 출발지점 위도 경도
        route.append(start_point)
        if i in (0, len(path) - 1): # 걷기에 대한 이동경로 정보
            b = a['steps']
            for j in range(len(b)):
                c = b[j]['linestring'].split(' ') # 걷기에 해당하는 위도,경도 리스트 추출
                for k in range(len(c)):
                    lon, lat = c[k].split(',') # 위도,경도를 route 리스트에 추가
                    route.append((float(lat), float(lon)))
        else: # 버스 혹은 지하철을 통한 이동경로 정보
            b = a['passShape']['linestring'].split(' ')
            for k in range(len(b)):
                lon, lat = b[k].split(',')
                route.append((float(lat), float(lon)))
        end_point = (a['end']['lat'], a['end']['lon'])
        route.append(end_point)
        # i번째 경로에 해당하는 정보를 담는 result
        result[f'{i}']['time'] = a['sectionTime']
        result[f'{i}']['type'] = a['mode'].lower()
        result[f'{i}']['path'] = route
    return result


# 지도 그리기
def draw_map(path_list, lgd_txt="<span style='color:{col};'>{txt}</span>"):
    start_point = path_list['0']['path'][0] # 출발지점 좌표
    end_point = path_list[f'{len(path_list) - 1}']['path'][-1] # 도착지점 좌표
    center = (start_point[0] + end_point[0]) / 2, (start_point[1] + end_point[1]) / 2 # 지도의 중심좌표
    color = {'walk': '#CCCCCC', 'bus': '#53B332', 'subway': '#0052A4', 'transfer': '#CCCCCC'}
    # 경로 지도 생성
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
# 좌표값을 주소로 역변환
def reverse_geo_coding(lat, lon, api_key):
    url = f"https://apis.openapi.sk.com/tmap/geo/reversegeocoding?version=1&lat={lat}&lon={lon}&coordType=WGS84GEO&addressType=A10&newAddressExtend=Y"

    headers = {
        "accept": "application/json",
        "appKey": 'OWYU6Tu4YP2Xt2Goijjb96P6ZdMoMJeS1OJJuX5v'
    }
    response = requests.get(url, headers=headers)
    result = json.loads(response.text)
    result = result['addressInfo']
    #'주소 추출'/'서울특별시' / '행정동' / '법정동' 추출
    juso,city_gu, admin_dong, legal_dong = result['fullAddress'].split(',')[2],result['city_do'] + ' ' + result['gu_gun'], result['adminDong'], result['legalDong']
    return juso,city_gu, admin_dong, legal_dong

# 걷기 경로 함수
# 목적지가 너무 가까워서 걷기로만 목적지에 도착하는 경우
def walk_route(dep_lat,dep_lon,des_lat,des_lon,destination,api_key):
    juso=reverse_geo_coding(dep_lat,dep_lon,api_key)[0]
    url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&callback=function"

    payload = {
        "startX": dep_lon, # 출발지 좌표
        "startY": dep_lat,
        "angle": 20, # 출발지와 도착지 사이의 각도(보행 방향)
        "speed": 5, # 평균 걸음 속도(km/h)
        "endPoiId": "10001",
        "endX": des_lon, # 도착지 좌표
        "endY": des_lat,
        "reqCoordType": "WGS84GEO",
        "startName": f"{quote(juso)}",
        "endName": f"{quote(destination)}", # 경로 탐색 옵션 (0은 기본값 추천)
        "searchOption": "0",
        "resCoordType": "WGS84GEO",
        "sort": "index"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "appKey": 'OWYU6Tu4YP2Xt2Goijjb96P6ZdMoMJeS1OJJuX5v'
    }

    response = requests.post(url, json=payload, headers=headers)
    response=json.loads(response.text)
    response=pd.DataFrame(response['features'])
    result=dict()
    # 걷기는 코드 0으로 구분
    result['0']=dict()
    result['0']['totalTime']=response['properties'][0]['totalTime']
    result['0']['type']='walk'
    result['0']['pathType']='walk' # pathType을 walk로 지정
    response=response['geometry']
    b=list()
    for i in range(len(response)):
        if response[i]['type']=='LineString':
            c=response[i]['coordinates'] # 경로에 해당하는 좌표 집합 추출
            for i in range(len(c)):
                d=c[i]
                e=(d[1],d[0])
                b.append(e)
    result['0']['path']=b # 걷기에 해당하는 경로 좌표 저장
    return result

# 최종 함수
# 최종 우편번호 추천
# 웹에서 사용자에게 받은 정보들로 필터링된 우편번호 값들을 인풋으로 이용
# 해당 우편번호 중 사용자가 희망하는 이동시간, 이동수단을 추가로 만족하는 우편번호와 추가정보 반환
# 우편번호가 다수일 시 이동시간이 적은 순서대로 반환
def final_recommend(dataset, zip_code_list, destination, limit_time, transfer_count, pathtype, api_key):
    result = dict()
    result_sample = dict()
    for i in range(len(zip_code_list)):
        
        dep_lat, dep_lon = dataset[zip_code_list[i]]['lat'], dataset[zip_code_list[i]]['lon']
        des_lat, des_lon = location_full(destination, api_key)
        print(i,des_lat,des_lon)
        # 사용자가 걷기를 선택한 경우
        if pathtype == 0 :
            a=walk_route(dep_lat,dep_lon,des_lat,des_lon,destination,api_key)
            c=walk_route(dep_lat,dep_lon,des_lat,des_lon,destination,api_key)
            c['totalTime']=c['0']['totalTime']
            c['pathType']=c['0']['pathType']
            # 이동수단별 소요시간 구하기
            walk_sum = 0
            bus_sum = 0
            subway_sum = 0
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
            # 사용자가 지하철, 버스, 지하철+버스를 선택한 경우
            b = route_condition_test(a, limit_time, transfer_count, pathtype)
            if b.shape[0] > 0:
                result[zip_code_list[i]] = dict()
                result_sample[zip_code_list[i]] = dict()
                c = b[b['totalTime'] == b['totalTime'].min()].iloc[0, :]
                path_list = Path_list(c['legs'])
                e = 0
                result[zip_code_list[i]]['totalTime'] = c['totalTime'] // 60
                
                for j in range(len(path_list)):
                    d = path_list[f'{j}']['type'] + f'{j+1}'
    
                    if j < len(path_list) - 1:
                        result[zip_code_list[i]][d] = path_list[f'{j}']['time'] // 60
                        result_sample[zip_code_list[i]][d] = path_list[f'{j}']['time'] // 60
                        e += result[zip_code_list[i]][d]
                    else:
                        
                        result[zip_code_list[i]][d] = result[zip_code_list[i]]['totalTime'] - e
                    
                # 이동수단별 소요시간 구하기
                walk_sum = 0
                bus_sum = 0
                subway_sum = 0
                for key, value in result[zip_code_list[i]].items():
                    if 'walk' in key:
                        walk_sum += value
                    elif 'bus' in key:
                        bus_sum += value
                    elif 'subway' in key:
                        subway_sum += value

                my_map = draw_map(path_list)
            else :
                continue
        folium.TileLayer('OpenStreetMap', name=f'{zip_code_list[i]}', min_zoom=12, max_zoom=16, control=True, opacity=0.7).add_to(my_map)
        folium.map.LayerControl('topleft', collapsed=False).add_to(my_map)
        city_gu, admin_dong, legal_dong = reverse_geo_coding(dep_lat, dep_lon, api_key)[1:]       
        # 주소정보
        result[zip_code_list[i]]['city_gu'] = city_gu
        result[zip_code_list[i]]['admin_dong'] = admin_dong
        result[zip_code_list[i]]['legal_dong'] = legal_dong
        # 이동수단
        result[zip_code_list[i]]['pathType'] = c['pathType']
        # 집값
        result[zip_code_list[i]]['avg_cost'] = round(dataset[zip_code_list[i]]['avg_cost'])
        # 이동수단별 소요시간
        result[zip_code_list[i]]['walk_sum'] = walk_sum
        result[zip_code_list[i]]['bus_sum'] = bus_sum
        result[zip_code_list[i]]['subway_sum'] = subway_sum
        # 지도 정보
        result[zip_code_list[i]]['map'] = my_map._repr_html_()
        
    try:
        # 이동시간이 적은 순서대로 정렬
        sorted_result = sorted(result.items(), key=lambda item: item[1]['totalTime'])
    except KeyError:
        sorted_result=dict()
    result = dict(sorted_result)
    
    return result

# 해당 우편번호의 500m 반경 카테고리들의 종류 및 위치 보여주는 함수모음

# 카테고리들의 좌표를 담고 있는 필드명
def category_list(default=0):
    result=['atm_info','pc_room_info','police_office_info','gonggogng_gym_info','perform_place_info',
             'park_info','church_info','big_mart_info','liberary_info','animal_hospital_info',
             'art_info', 'banchan_info', 'bus_stop_info', 'hospital_info', 'beauty_care_info',
             'daiso_info', 'chatolic_info', 'shopping_center_info', 'bar_info', 'super_market_info',
             'pharmacy_info', 'theater_info', 'yoga_info', 'post_office_info', 'bank_info', 'food_store_info',
             'bike_info', 'temple_info', 'citizen_center_info', 'subway_info', 'cafe_info', 'coin_karaoke_info',
             'coin_wash_room_info', 'cross_fit_info', 'convience_store_info', 'piilates_info', 'gym_info']
    return result

# 지도에 카테고리별로 다른 색상을 부여하기 위한 과정
def color_book(default=0):
    result={'bus_stop': {'color': 'blue', 'icon': 'bus-simple'},
            'art': {'color': 'green', 'icon': 'palette'},
            'bike': {'color': 'green', 'icon': 'bicycle'},
            'hospital': {'color': 'red', 'icon': 'house-medical'},
            'animal_hospital': {'color': 'red', 'icon': 'paw'},
            'theater': {'color': 'green', 'icon': 'film'},
            'subway': {'color': 'blue', 'icon': 'subway'},
            'big_mart': {'color': 'green', 'icon': 'shopping-cart'},
            'bar': {'color': 'orange', 'icon': 'beer-mug-empty'},
            'shopping_center': {'color': 'orange', 'icon': 'shopping-bag'},
            'pharmacy': {'color': 'green', 'icon': 'pills'},
            'bank': {'color': 'green', 'icon': 'krw'},
            'atm': {'color': 'gray', 'icon': 'krw'},
            'food_store': {'color': 'orange', 'icon': 'cutlery'},
            'banchan': {'color': 'orange', 'icon': 'cutlery'},
            'coin_karaoke': {'color': 'green', 'icon': 'microphone-lines'},
            'cafe': {'color': 'darkred', 'icon': 'coffee'},
            'citizen_center': {'color': 'green', 'icon': 'institution'},
            'police_office': {'color': 'blue', 'icon': 'institution'},
            'post_office': {'color': 'green', 'icon': 'envelope-open'},
            'pc_room': {'color': 'green', 'icon': 'computer'},
            'super_market': {'color': 'orange', 'icon': 'store'},
            'convience_store': {'color': 'lightblue', 'icon': 'shop'},
            'beauty_care': {'color': 'green', 'icon': 'shopping-basket'},
            'daiso': {'color': 'green', 'icon': 'shopping-basket'},
            'gonggogng_gym': {'color': 'green', 'icon': 'futbol'},
            'park': {'color': 'green', 'icon': 'tree'},
            'liberary': {'color': 'green', 'icon': 'book'},
            'gym': {'color': 'green', 'icon': 'dumbbell'},
            'yoga': {'color': 'green', 'icon': 'shoe-prints'},
            'cross_fit': {'color': 'green', 'icon': 'stopwatch-20'},
            'piilates': {'color': 'green', 'icon': 'shoe-prints'},
            'perform_place': {'color': 'green', 'icon': 'video-camera'},
            'church': {'color': 'lightgray', 'icon': 'church'},
            'chatolic': {'color': 'lightgray', 'icon': 'cross'},
            'temple': {'color': 'lightgray', 'icon': 'person-praying'},
            'coin_wash_room': {'color': 'green', 'icon': 'coins'}}
    return result
# 영어로 된 필드명을 사용자에게 한국어로 보여주기 위한 과정
def name_change(default=0):
    result={'bus_stop': '버스정류장',
            'art': '미술관 & 전시관',
            'bike': '자전거대여소',
            'gym': '헬스클럽',
            'chatolic': '성당',
             'hospital': '병원',
             'perform_place': '공연장',
             'park': '공원',
             'theater': '영화관',
             'subway': '지하철',
             'animal_hospital': '동물병원',
             'beauty_care': '뷰티케어',
             'coin_karaoke': '코인노래방',
             'liberary': '도서관',
             'church': '교회',
             'big_mart': '대형마트',
             'gonggogng_gym': '공공체육시설',
             'cafe': '카페 & 디저트',
             'police_office': '경찰서',
             'daiso': '생활용품점',
             'bar': '술집',
             'shopping_center': '쇼핑센터',
             'super_market': '슈퍼마켓',
             'pharmacy': '약국',
             'banchan': '반찬가게 & 밀키트',
             'convience_store': '편의점',
             'bank': '은행',
             'coin_wash_room': '코인세탁방',
             'yoga': '요가',
             'cross_fit': '크로스핏',
             'atm': 'ATM',
             'food_store': '음식점',
             'post_office': '우체국',
             'pc_room': 'PC방',
             'piilates': '필라테스',
             'citizen_center': '주민센터',
             'temple': '절'}
    return result

# 우편번호의 500m 반경에 위치하는 카테고리들의 위치 시각화
# 사용자가 선호하는 카테고리를 우선적으로 보여줌
def facility_map(dict_file,check_list):
    result=dict()
    color_icon=color_book() # 색깔 지정
    name_book=name_change() # 한국어로 보여주기
    lgd_txt="<span style='color:{col};'>{txt}</span>"

    for zip_code in dict_file.keys(): 
        categories=category_list() # 필드명 불러오기
        facility_info=dict_file[zip_code] # 우편번호별 카테고리 정보들 저장
        center=(facility_info['lat'],facility_info['lon']) #해당 우편번호의 중심좌표
        my_map=folium.Map(location=center,zoom_start=16,tiles=None)
        result[zip_code]=dict()
    #opacity: 지도 배경의 불투명도
        folium.TileLayer('OpenStreetMap',min_zoom=14,max_zoom=18,name=f'{zip_code}',control=False,opacity=0.7).add_to(my_map)
    #체크박스(500m원)
        fg_center=folium.FeatureGroup(name=lgd_txt.format(col='lightblue',txt='500M'))
    #500m 원(color:테두리색,fill_color:속 색, opacity: 테두리 불투명도, fill_opacity: 속 색 불투명도)
        folium.Circle(location=center,radius=500,color='black',fill_color='#008fff',opacity=0.1,fill_opacity=0.2).add_to(fg_center)
    #체크박스(우편번호글씨와 구역화 두개를 한번에 껐다켤수있음)
        fg_zipcode=folium.FeatureGroup(name=lgd_txt.format(col='#696969',txt=f'{zip_code}'))
    #지도 속 우편번호 글자 조정(font-size: 글자 크기, color: 글자 색)
        folium.Marker(location=center,icon=folium.DivIcon(html=f'<div style="font-size:25px;background-color:rgba(0, 0, 0, 0);color:#696969;">{zip_code}</div>')).add_to(fg_zipcode)
    #만약 중심 넣고 싶으면 radius랑 fill_opacity 수정)
        folium.Circle(location=center,radius=20,color='red',fill_color='blue',fill_opacity=0,opacity=0).add_to(fg_zipcode)
        fg_center.add_to(my_map)
        fg_zipcode.add_to(my_map)
        # 사용자에게 선택되지 않은 카테고리들 처리
        for check in check_list:
            category=check+'_info'
            coordinates=facility_info[category] 
            coordinates=json.loads(coordinates) # 특정 우편번호의 특정 시설의 좌표 리스트 저장
            # 지도에 표시하기 위한 과정
            color=color_icon[check]['color']
            icon=color_icon[check]['icon']
            fg_point=folium.FeatureGroup(name=lgd_txt.format(col=color,txt=f"{name_book[check]} : {len(coordinates)}개"))
            # 리스트 안에 있는 모든 좌표들 지도에 찍기
            for coordinate in coordinates:
                marker=folium.Marker(location=coordinate,icon=folium.Icon(color=color, icon=icon, prefix="fa",shadow=False),popup=None)
                marker.add_to(fg_point)
            fg_point.add_to(my_map)
            result[zip_code][check]=len(coordinates)
            categories.remove(category)
        # 사용자에게 받은 선호 리스트 처리 과정
        for category in categories:
            if type(json.loads(facility_info[category]))==list: # 해당 우편번호 500m 반경에 카테고리가 존재하는 경우
                check=category[:-5] # 위에서 붙였던 '_info' 제거 ( 사용자에게 받은 경우 필드에 _info가 붙어있지 않기 때문)
                coordinates=facility_info[category]
                coordinates=json.loads(coordinates)
                color=color_icon[check]['color']
                icon=color_icon[check]['icon']
                fg_point=folium.FeatureGroup(name=lgd_txt.format(col=color,txt=f"{name_book[check]} : {len(coordinates)}개"))
                for coordinate in coordinates:
                    marker=folium.Marker(location=coordinate,icon=folium.Icon(color=color, icon=icon, prefix="fa",shadow=False),popup=None)
                    marker.add_to(fg_point)
                fg_point.add_to(my_map) 
                #result[zip_code][check]=len(coordinates)
        folium.map.LayerControl('topleft', collapsed= False).add_to(my_map)
        # 사용자에게 선택받지 않는 카테고리들은 지도 상에 체크되지 않은 채로 시작
        start_unchecked_from = 2+len(check_list)
        js_code = f"""
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    var checkBoxes = document.querySelectorAll('.leaflet-control-layers-selector');
                    for(var i={start_unchecked_from}; i<checkBoxes.length; i++) {{
                        checkBoxes[i].click();
                    }}
                }});
            </script>
        """
        my_map.get_root().html.add_child(folium.Element(js_code))
        # 최종 지도 생성
        result[zip_code]['map2']=my_map._repr_html_()
    
    return result