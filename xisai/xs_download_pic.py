from xisai.subject import connDB
import requests
import os

if __name__ == '__main__':


    picFilePath = '/Users/xiang/xiang/study/Python/selenium_python/pic/xisai/'

    try:
        conn = connDB.getConn()
        cursor = conn.cursor()

        # 查询表 s_pic 中的图片 URL
        cursor.execute("SELECT id, pic_url FROM s_pic")
        rows = cursor.fetchall()

        # 遍历查询结果
        for row in rows:

            if isinstance(row, dict):
                pic_id = row['id']  # 使用键 'id' 获取 id 字段
                pic_url = row['pic_url']  # 使用键 'pic_url' 获取 pic_url 字段
            else:
                pic_id = row[0]  # 使用索引 0 获取 id 字段
                pic_url = row[1]  # 使用索引 1 获取 pic_url 字段

            # # 下载图片
            try:
                r = requests.get(pic_url, stream=True)
                r.raise_for_status()

                # 构造本地文件名，假设从 URL 中获取文件名
                filename = os.path.join(picFilePath, os.path.basename(pic_url))

                # 写入文件
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f"Downloaded {filename}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading {pic_url}: {e}")

        print(f"Error connecting to MySQL: {e}")

    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()