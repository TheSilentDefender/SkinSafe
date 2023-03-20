import clientPromise from '@/lib/mongodb';

export default async (req: any, res: { json: (arg0: any) => void }) => {
  try {
    const searchQuery = req.query.search;
    if (!searchQuery) {
      fetch('https://skin-safe.vercel.app/api/allproducts')
        .then((response) => {
          return response.json();
        }
        )
    }
    const client = await clientPromise;
    const collection = client.db('products').collection('ulta');
    const searchResults = await collection.aggregate([
      {
        $search: {
          index: "default",
          text: {
            query: "skin",
            path: {
              wildcard: "*"
            }
          }
        }
      }
    ]).toArray();
    res.json(searchResults);
  } catch (e) {
    console.error(e);
  }
};
