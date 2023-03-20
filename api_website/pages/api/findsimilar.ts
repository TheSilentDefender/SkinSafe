import { ObjectId } from "mongodb";

export default async (req: any, res: { json: (arg0: any) => void }) => {
  try {
    const { productIds } = req.body;
    let products = await fetchProducts(productIds);
    // concat the products
    products = products.flat();
    // sort by similarity
    products.sort((a: any, b: any) => b.similarity - a.similarity);
    products = products.slice(0, 10);
    res.json(products);
  } catch (e) {
    console.error(e);
  }
};

export interface ProductProps {
  _id: ObjectId;
  brand: string;
  category: string;
  name: string;
  color: number | undefined;
  ingredients: string[];
  product_url: string;
}

async function fetchProducts(productIds: ObjectId[]) {
  const results: ProductProps[] = [];
  for (const productId of productIds) {
    const product = await fetchProduct(productId);
    results.push(product);
  }
  return results;
}

async function fetchProduct(productId: ObjectId): Promise<ProductProps> {
  const data = await fetch('http://localhost:3000/api/allproducts').then(
    (response) => response.json()
  );

  const inputProd = data.find((product: ProductProps) => product._id === productId);

  const similarities = data.map((product : ProductProps) => {
    return calculateSimilarity(inputProd.ingredients, product.ingredients);
  });

  for (let i = 0; i < data.length; i++) {
    data[i].similarity = similarities[i];
  }

  data.sort((a: any, b: any) => b.similarity - a.similarity);
  
  for (let i = 0; i < data.length; i++) {
    if (data[i].similarity === 1) {
      data.splice(i, 1);
    }
  }

  data.splice(0, 1);
  return data.slice(0, 10);
}

function calculateSimilarity(arr1: string[], arr2: string[]): number {
  const set1 = new Set(arr1);
  const set2 = new Set(arr2);
  const intersection = new Set([...set1].filter((x) => set2.has(x)));
  const union = new Set([...set1, ...set2]);
  const similarity = intersection.size / union.size;
  return similarity;
}
