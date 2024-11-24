## sjoin_bldg_and_zone.py
## 建物ポリゴンに対して重なっている用途地域ポリゴンのID値を空間結合するスクリプト

import geopandas as gpd
from shapely.geometry import Point

import re
import glob

def sjoin_bldg_and_zone(filepath):
    file_num=re.search(r"(\d+)", filepath).group(1)

    # 建物ポリゴンの読み込み
    building_polygons = gpd.read_file(filepath)

    # 用途地域ポリゴンの読み込み
    zone_polygons_jgd2011 = gpd.read_file('urf_6697_op.geojson')

    building_polygons.set_crs(epsg=4326, allow_override=True)
    zone_polygons = zone_polygons_jgd2011.to_crs(epsg=4326)

    # ポリゴンジオメトリを一旦記憶
    building_polygons['polygeom']=building_polygons.geometry
    # 低精度重心を GeoDataFrame に追加する
    building_polygons["centroid"] = building_polygons["polygeom"].centroid
    #ジオメトリを交換
    building_polygons = building_polygons.set_geometry('centroid')

    # 空間結合を実行
    joined_polygons = gpd.sjoin(building_polygons, zone_polygons, how="left", predicate="within")
    joined_polygons = joined_polygons.set_geometry('polygeom')

    #不要な列を取り除く
    joined_dataframe = joined_polygons.drop(columns=[
        'geometry',
        'centroid',
        'polygeom',
        'index_right',
        'id_right',
        'layer',
        'path'
    ]).rename(columns={
        'id_left': 'id',
        'measuredHeight': 'measuredHeight',  # 名前変更なし
        'function': 'function'  # 名前変更なし
    })

    geodataframe = gpd.GeoDataFrame(data=joined_dataframe, geometry=joined_polygons.geometry, 
    crs=joined_polygons.crs)
    #　urf/geojsonファルダに新しいGeoJSONを保存
    # 環境に応じてパスを要修正
    saved_path=f'urf/geojson/{file_num}.geojson'
    geodataframe.to_file(saved_path, driver='GeoJSON')
    return saved_path

def main():
    # bldg/geojsonフォルダのすべての`*.geojson`ファイルを対象
    # 環境に応じてパスを要修正
    target_filepath = "bldg/geojson/*.geojson"

    file_paths=glob.glob(target_filepath, recursive=False)   
    files_len=len(file_paths)
    for i, filepath in enumerate(file_paths):   
        #ファイルごとに空間結合処理関数を呼ぶ        
        save_path=sjoin_bldg_and_zone(filepath)
        print(f"{i+1}/{files_len} Saved:{save_path}")

if __name__ == "__main__":
    main()