import chromadb

client=chromadb.PersistentClient(path="./chroma-db")
collection= client.get_or_create_collection(
      name="remote_work"
)
