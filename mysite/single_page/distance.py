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

#정민
#api_key='jWKJB0EUmw8Bq7MWSEdBR9CHS1MXzX6j9q5wZ5Mv'
#기웅
#api_key='XfJ1aYM2eI8nMlTSPZFqO9bOGndL7eS87UvsOvUj'
#t-map api_key
#api_key ='7qu49yhCse9cOGrEMAAzT4vFpf5THX6y4eOeE1ch'
#t-map 대중교통 api_key_지율
#api_key='mHGFWgLaqA2SSvNlXlOKWasFge3VLc301ObkglfC'

def location_full(addr,api_key):
    #UTF-8기반 URL encoding
    addr=quote(addr)
    url = f"https://apis.openapi.sk.com/tmap/geo/fullAddrGeo?version=1&fullAddr={addr}"
    headers = {
        "accept": "application/json",
        "appKey": api_key
    }
    response = requests.get(url, headers=headers)
    response = json.loads(response.text)
    lat=float(response['coordinateInfo']['coordinate'][0]['newLat'])
    lon=float(response['coordinateInfo']['coordinate'][0]['newLon'])
    return (lat,lon)

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
    result=json.loads(response.text)
    result=result['metaData']['plan']['itineraries']
    return result

def route_condition_test(route,limit_time,transfer_count,pathtype):
    a=pd.DataFrame(route)
    if pathtype==3:
        result=a[(a['totalTime']<=limit_time*60)&(a['transferCount']<=transfer_count)]
    else :
        result=a[(a['totalTime']<=limit_time*60)&(a['transferCount']<=transfer_count)&(a['pathType']==pathtype)]
    return result

#지도 그리기 준비1
def Path_list(path):
    result=dict()
    for i in range(len(path)):
        a=path[i]
        result[f'{i}']={}
        route=[]
        start_point=(a['start']['lat'],a['start']['lon'])
        route.append(start_point)
        if i in (0,len(path)-1):
            b=a['steps']
            for j in range(len(b)):
                c=b[j]['linestring'].split(' ')
                for k in range(len(c)):
                    lon,lat=c[k].split(',')
                    route.append((float(lat),float(lon)))
        else:
            b=a['passShape']['linestring'].split(' ')
            for k in range(len(b)):
                lon,lat=b[k].split(',')
                route.append((float(lat),float(lon)))
        end_point=(a['end']['lat'],a['end']['lon'])
        route.append(end_point)
        result[f'{i}']['time']= a['sectionTime']
        result[f'{i}']['type']= a['mode'].lower()
        result[f'{i}']['path']=route
    return result

#지도 그리기
def draw_map(path_list,lgd_txt="<span style='color:{col};'>{txt}</span>"):
    start_point=path_list['0']['path'][0]
    end_point=path_list[f'{len(path_list)-1}']['path'][-1]
    center=(start_point[0]+end_point[0])/2,(start_point[1]+end_point[1])/2
    color={'walk':'#CCCCCC','bus':'#53B332','subway':'#0052A4','transfer':'#CCCCCC'}
    my_map=folium.Map(location=center,zoom_start=14,tiles=None)
    fg_start_point=folium.FeatureGroup(name=lgd_txt.format(col='green',txt="출발"))
    start_marker=folium.Marker(location=start_point,icon=folium.Icon(color="green", icon="play", prefix="fa"))
    fg_end_point=folium.FeatureGroup(name=lgd_txt.format(col='red',txt="도착"))
    end_marker=folium.Marker(location=end_point,icon=folium.Icon(color="red", icon="stop", prefix="fa"))
    circle_layer=folium.Circle(location=start_point,radius=500,color=None,fill_color='#CE21FA',opacity=0.3,fill=True)
    start_marker.add_to(fg_start_point)
    end_marker.add_to(fg_end_point)
    circle_layer.add_to(fg_start_point)
    fg_start_point.add_to(my_map)
    for i in range(len(path_list)):
        fg_route=folium.FeatureGroup(name=lgd_txt.format(col=color[path_list[f'{i}']['type']],txt=f"{path_list[f'{i}']['type']}{i+1}"))
        route_1=folium.PolyLine(locations=path_list[f'{i}']['path'], color='#696969', weight=10)
        route_2=folium.PolyLine(locations=path_list[f'{i}']['path'], color=color[path_list[f'{i}']['type']], weight=6)
        route_1.add_to(fg_route)
        route_2.add_to(fg_route)
        fg_route.add_to(my_map)
    fg_end_point.add_to(my_map)
    return my_map

#reverse_geocoding
def reverse_geo_coding(lat,lon,api_key) :
    url = f"https://apis.openapi.sk.com/tmap/geo/reversegeocoding?version=1&lat={lat}&lon={lon}&coordType=WGS84GEO&addressType=A10&newAddressExtend=Y"

    headers = {
        "accept": "application/json",
        "appKey": api_key
    }
    response = requests.get(url, headers=headers)
    result=json.loads(response.text)
    result=result['addressInfo']
    city_gu,admin_dong,legal_dong=result['city_do']+' '+result['gu_gun'],result['adminDong'],result['legalDong']
    return city_gu,admin_dong,legal_dong

#zip_code의 정보를 담은 dict 만들기 / 데이터셋<df 가정>
def recommend_zip_code(dataset, zip_code, destination, limit_time, transfer_count, pathtype,api_key):
    dep_lat,dep_lon=dataset[zip_code]['lat'],dataset[zip_code]['lon']
    des_lat,des_lon=location_full(destination,api_key)
    a=commute_route(dep_lat,dep_lon,des_lat,des_lon,api_key)
    b=route_condition_test(a,limit_time,transfer_count,pathtype)
    if b.shape[0] > 0 :
        c=b[b['totalTime']==b['totalTime'].min()].iloc[0,:]
        path_list=Path_list(c['legs'])
        my_map=draw_map(path_list)
        folium.TileLayer('OpenStreetMap', name=f'{zip_code}',min_zoom=12,max_zoom=16,control=True,opacity=0.7).add_to(my_map)
        folium.map.LayerControl('topleft', collapsed= False).add_to(my_map)
        city_gu, admin_dong, legal_dong = reverse_geo_coding(dep_lat,dep_lon,api_key)
        result=dict()
        result['city_gu']=city_gu
        result['admin_dong']=admin_dong
        result['legal_dong']=legal_dong
        result['totalTime']=c['totalTime']//60
        e=0
        for i in range(len(path_list)):
            d=path_list[f'{i}']['type']+f'{i+1}'
            if i < len(path_list)-1:
                result[d]=path_list[f'{i}']['time']//60
                e+=result[d]
            else :
                result[d]=result['totalTime']-e
        result['pathType']=c['pathType']
        result['map']=my_map
    else :
        result=list()
    return result

#최종 함수
def final_recommend(dataset,zip_code_list,destination,limit_time, transfer_count, pathtype,api_key):
    result=dict()
    for i in range(len(zip_code_list)):
        a=recommend_zip_code(dataset,zip_code_list[i],destination,limit_time,transfer_count,pathtype,api_key)
        if type(a)==dict:
            result[zip_code_list[i]]=a
    return result

#만약 api_key_list를 만들거라면
def final_recommend_api_key_list(dataset,zip_code_list,destination,limit_time, transfer_count, pathtype,api_key_list):
    result=dict()
    api_times=0
    for i in range(len(zip_code_list)):
        try:
            api_key=api_key_list[api_times//10]
            a=recommend_zip_code(dataset,zip_code_list[i],destination,limit_time,transfer_count,pathtype,api_key)
            api_times+=1
            if type(a)==dict:
                result[zip_code_list[i]]=a
        except KeyError:
            break
    return result

#돌리면 돌아감
#api 다 쓰면 commute_route에서 KeyError가 뜸!!!
X=pd.read_csv('최종데이터셋_500m기준.csv')
X['우편번호']=X['우편번호'].apply(lambda x: '0'+str(x))
df={}
df['03934']={'lat':X.loc[269,'위도'],'lon':X.loc[269,'경도']}
df['03977']={'lat':X.loc[303,'위도'],'lon':X.loc[303,'경도']}
df['03930']={'lat':X.loc[267,'위도'],'lon':X.loc[267,'경도']}
df['03726']={'lat':X.loc[218,'위도'],'lon':X.loc[218,'경도']}


gift=final_recommend(df,['03934','03930','03977'],'서울특별시 마포구 와우산로 94',limit_time=30,transfer_count=0,pathtype=3,api_key=api_key)
print(gift)