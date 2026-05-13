import sqlite3

conn = sqlite3.connect('data/processed/health_analytics.db')

with open('scripts/advanced_queries.sql', 'r') as f:
    content = f.read()

# Split by -- Query to get individual queries
blocks = content.split('-- Query')
queries = []
for block in blocks[1:]:  # skip first empty block
    lines = block.strip().split('\n')
    title = lines[0].strip()
    sql = '\n'.join(lines[1:]).strip().rstrip(';')
    if sql:
        queries.append((title, sql))

for title, query in queries:
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        print(f"\n✅ Query {title}")
        print("  " + " | ".join(col_names))
        print("  " + "-" * 50)
        for row in rows[:3]:  # show first 3 rows only
            print("  " + " | ".join(str(x) for x in row))
    except Exception as e:
        print(f"\n❌ Query {title}: {e}")

conn.close()
print("\n🎉 Done!")