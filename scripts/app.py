from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

# 创建客户端
ip_addr = "localhost"             
client = QdrantClient(
    url=f"http://{ip_addr}:6333",
    api_key="123456"
)

# 创建索引
def create_collection():
    collection_name = "test_collection"
    # 检查集合是否已存在，避免重复创建
    try:
        client.get_collection(collection_name)
        print(f"✅ Collection '{collection_name}' already exists!")
    except Exception:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=4, distance=Distance.DOT),
        )
        print(f"✅ Collection '{collection_name}' created successfully!")

# 添加数据
def add_data():
    points = [
        PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
        PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
        PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
        PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
        PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
        PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
    ]

    operation_info = client.upsert(
        collection_name="test_collection",
        wait=True,
        points=points,
    )

    # 返回值
    print(f"✅ Data added successfully! Status: {operation_info.status}")

# 查询数据
def query_data():
    search_result = client.query_points(
        collection_name="test_collection",
        limit=3,
        with_payload=True,
        query=[0.2, 0.1, 0.9, 0.7],  # 使用 query 参数
    ).points

    # 打印查询结果
    print("🔍 查询结果：")
    for result in search_result:
        print(f"id={result.id} score={result.score} payload={result.payload}")

# 带过滤条件查询
def filter_data():
    search_result = client.query_points(
        collection_name="test_collection",
        limit=3,
        with_payload=True,
        query=[0.2, 0.1, 0.9, 0.7],  # 使用 query 参数
        query_filter=Filter(
            must=[FieldCondition(key="city", match=MatchValue(value="London"))]
        )
    ).points

    # 打印过滤结果
    print("🔍 过滤结果：")
    for result in search_result:
        print(f"id={result.id} score={result.score} payload={result.payload}")

if __name__ == '__main__':
    # 1. 创建索引
    create_collection()

    # 2. 添加数据
    add_data()

    # 3. 查询数据
    query_data()

    # 4. 过滤数据
    filter_data()
