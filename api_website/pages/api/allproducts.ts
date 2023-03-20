import clientPromise from '@/lib/mongodb';
import { ObjectId } from 'mongodb';

export interface ProductProps {
  _id: ObjectId;
  brand: string;
  category: string;
  name: string;
  color: number | undefined;
  ingredients: string[];
  product_url: string;
}


export default async (req: any, res: { json: (arg0: any) => void; }) => {
  try {
    const client = await clientPromise;
    const collection = client.db('products').collection('ulta');
    const cursor = await collection.find({});
    const products = await cursor.toArray();
    res.json(products);    
  } catch (e) {
      console.error(e);
  }
};