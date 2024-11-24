## convert_to_geojson.py
## PLATEAUのCityGMLファイルから必要な要素を抽出しGeoJSONで保存するスクリプト

#ライブラリをインポート
import glob
import xml.etree.ElementTree as ET　#XMLパースライブラリ
import re
import json

# GMLから要素を抽出
def get_raw_obj(filepath):
    raw_obj=[]
    # GMLを読む
    tree = ET.parse(filepath)
    root = tree.getroot() #ルートを取得
    for bldg in root.iter('{http://www.opengis.net/citygml/building/2.0}Building'):　#URL付きタグ名で建物取得
        
        #建物座標を取得
        foot_print=bldg.find('{http://www.opengis.net/citygml/building/2.0}lod0FootPrint')

        #座標データがbldg傘下にある場合
        if foot_print is not None:
            # 建物オブジェクトを宣言
            bldg_obj={}
            bldg_obj['coord_raw']=[]

            for pos_list in foot_print.iter('{http://www.opengis.net/gml}posList'):        
                bldg_obj['coord_raw'].append(pos_list.text)

            # 建物高さを取得
            bldg_obj['height']=0
            m_heights=bldg.iter('{http://www.opengis.net/citygml/building/2.0}measuredHeight')
            for m_height in m_heights:
                if m_height is not None:
                    bldg_obj['height']=m_height.text
                    break
            raw_obj.append(bldg_obj)
            
        else:
            # BuildingPartとして複数ある場合
            parts=bldg.iter('{http://www.opengis.net/citygml/building/2.0}BuildingPart')
            for part in parts:
                # 建物オブジェクトを宣言
                bldg_obj={}
                bldg_obj['coord_raw']=[]

                #建物座標を取得
                foot_print=part.find('{http://www.opengis.net/citygml/building/2.0}lod0FootPrint')
                if foot_print is not None:
                    for pos_list in foot_print.iter('{http://www.opengis.net/gml}posList'):        
                        bldg_obj['coord_raw'].append(pos_list.text)

                    # 建物高さを取得
                    bldg_obj['height']=0
                    m_heights=part.iter('{http://www.opengis.net/citygml/building/2.0}measuredHeight')
                    for m_height in m_heights:
                        if m_height is not None:
                            bldg_obj['height']=m_height.text
                            break
                    raw_obj.append(bldg_obj)
    # 抽出要素を返す
    return raw_obj 

# 抽出要素からgeojsonを作成し保存
def save_geojson(filepath, raw_obj):
    file_num=re.search(r"(\d+)", filepath).group(1)
    
    # テンプレート定義
    geojson = {
        "type": "FeatureCollection",
        "name": f"{file_num}",
        "features": []  # ここにfeaturesを入れる
    }


    # データをパースしてGeoJSONの構造に変換
    for i, item in enumerate(raw_obj):
        
        #座標データの構造を作成
        coords = item['coord_raw'][0].strip().split(' ')
        coordinates = [
            [
                [float(coords[j+1]), float(coords[j])]
                for j in range(0, len(coords), 3)
            ]
        ]
        #GeoJSONデータの構造を作成
        feature = {
            "type": "Feature",
            "id": f"{file_num}-{i}",
            "properties": {
                "measuredHeight": float(item['height'])
            },
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [coordinates]
            }
        }
        geojson["features"].append(feature)
    # bldg/geojsonフォルダにGeoJSONファイルとして保存
    # 環境に応じてパスを要修正
    save_path=f"bldg/geojson/{file_num}.geojson"
    with open(save_path, "w") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=4)
    return save_path
    

def main():

    # bldgフォルダ直下のすべての`*.gml`ファイルを対象
    # 環境に応じてパスを要修正
    target_filepath = "bldg/*.gml"

    file_paths=glob.glob(target_filepath, recursive=False)   
    files_len=len(file_paths)
    for i, filepath in enumerate(file_paths):           
        save_path=save_geojson(filepath, get_raw_obj(filepath))
        print(f"{i+1}/{files_len} Saved:{save_path}")

if __name__ == "__main__":
    main()