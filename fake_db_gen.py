from db_manager import DataBaseManager
import duckdb
import sqlite3 # DB Base

conn = duckdb.connect('minerank.db')
DB = DataBaseManager(cursor=conn.cursor())

# 커뮤니티 게시물 ID null 수정
print("\n=== Fixing community_posts with null IDs ===")
try:
    cursor = conn.cursor()
    
    # null ID를 가진 게시물 조회
    cursor.execute("SELECT serverId, userId, title, content, timestamp, views, recommendations FROM community_posts WHERE id IS NULL")
    null_id_posts = cursor.fetchall()
    
    if null_id_posts:
        print(f"Found {len(null_id_posts)} posts with null IDs")
        
        # 먼저 null ID 게시물 삭제
        cursor.execute("DELETE FROM community_posts WHERE id IS NULL")
        
        # 다음 사용 가능한 ID 찾기
        cursor.execute("SELECT COALESCE(MAX(id), 0) FROM community_posts")
        result = cursor.fetchone()
        max_id = result[0] if result else 0
        next_id = max_id + 1
        
        # 다시 올바른 ID로 삽입
        for post in null_id_posts:
            cursor.execute(
                '''INSERT INTO community_posts (id, serverId, userId, title, content, timestamp, views, recommendations)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                [next_id, post[0], post[1], post[2], post[3], post[4], post[5], post[6]]
            )
            print(f"  - Fixed post: ID {next_id}, title: '{post[2][:30]}...'")
            next_id += 1
        
        print(f"Successfully fixed {len(null_id_posts)} posts")
    else:
        print("No posts with null IDs found")
        
except Exception as e:
    print(f"Error fixing community posts: {e}")

print("\n=== Database setup complete ===")
conn.close()