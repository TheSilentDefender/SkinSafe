import { useState, useEffect } from 'react';
import { GetImage } from '@/components/scrapeImage';
import { ObjectId } from 'mongodb';

type Product = {
  _id: string;
  brand: string;
  category: string;
  name: string;
  color: string;
  ingredients: string[];
  product_url: string;
};

export default function Home() {
  const [search, setSearch] = useState('');
  const [selectedProducts, setSelectedProducts] = useState<Product[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [compareData, setCompareData] = useState<any>(null);

  const handleCompareProducts = async () => {
    document.getElementById('compareButton').innerHTML = 'Loading...';
    const productIds = selectedProducts.map((product) => product._id);
    console.log(productIds);
    const response = await fetch('/api/findsimilar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ productIds })
    });
    const data = await response.json();
    // json to array
    console.error(data);
    setCompareData(data);
    setIsModalOpen(true);
    document.getElementById('compareButton').innerHTML = 'Compare';
  };

  const closeCompareProducts = async () => {
    setIsModalOpen(false);
  };

  useEffect(() => {
    fetch('http://localhost:3000/api/searchproduct?search=' + search)
      .then((response) => response.json())
      .then((data) => setProducts(data));
  }, []);

  const filteredProducts = products.filter((product) =>
    product.name.toLowerCase().includes(search.toLowerCase())
  );

  const handleAddProduct = (product: Product) => {
    // Check if product already exists in selectedProducts
    if (!selectedProducts.find((p) => p._id === product._id)) {
      setSelectedProducts([...selectedProducts, product]);
    }
  };

  return (
    <div className="flex bg-transparent">
      <div className="w-1/2 p-8">
        <h1 className="bg-clip-text bg-gradient-to-b from-purple-300 via-white to-blue-300 border-b my-3 py-3 font-bold text-6xl text-transparent">SkinSafe</h1>
        <div className="flex mb-4">
          <input
            className="w-full rounded-lg"
            type="text"
            placeholder="Search products"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <ul className="h-[75vh] overflow-hidden overflow-y-scroll">
          {filteredProducts.map((product) => {
            console.warn(product._id);
            return (
              <li
                key={product._id}
                className="flex items-center transition-bg-opacity duration-300 mb-2 bg-black bg-opacity-20 hover:bg-opacity-40 p-2 rounded-xl "
              >
                <div className="flex-1 text-white ">
                  <div className="font-bold">{product.brand}</div>
                  <a
                    href={product.product_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-white hover:text-blue-400"
                  >
                    {product.name}
                  </a>
                </div>
                <button
                  className="transition-bg duration-300 rounded-xl border-2 border-white bg-transparent hover:bg-blue-600 text-white font-bold py-2 px-4 ml-2 rounded"
                  onClick={() => handleAddProduct(product)}
                >
                  Add
                </button>
              </li>
            );
          })}
        </ul>
      </div>
      <div className="w-1/2 p-8">
        <h2 className="text-white text-xl font-bold my-5">Selected Products</h2>
        <ul className="h-[80vh] overflow-hidden overflow-y-scroll">
          {selectedProducts.map((product) => (
            <li
              key={product._id}
              className="flex items-center mb-2 bg-black bg-opacity-20 p-2 rounded-2xl "
            >
              <div className="flex-1 text-white">{product.name}</div>
              <GetImage url={product.product_url} name={product.name} />
            </li>
          ))}
        </ul>
        <button
          id="compareButton"
          className="transform-bg duration-200 bg-blue-600 hover:bg-blue-400 text-white font-bold py-2 px-4 w-full rounded-lg"
          onClick={handleCompareProducts}
        >
          Compare
        </button>

        {isModalOpen && (
          <div className="m-20 items-center justify-center fixed z-10 inset-0">
            <div className="flex items-center justify-center h-full m-10">
              <div className="flex flex-col items-center  bg-white p-6 rounded-2xl h-full w-auto overflow-hidden overflow-y-scroll">
                <h2 className="mb-4"><b>Comparison Results</b></h2>
                {compareData.map((product: any) => (
                  <div className="w-full">
                    <div className="flex items-center justify-center mb-2  bg-slate-100 p-2 rounded-2xl ">
                      <div className="flex-1 text-black"><b>{product.brand}</b><br />{product.name}</div>
                      <GetImage url={product.product_url} name={product.name} />
                    </div>
                  </div>
                ))}
                <button
                  className="bg-black hover:bg-blue-600 text-white font-bold py-2 px-4 mt-4 rounded"
                  onClick={closeCompareProducts}
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export interface ProductProps {
  _id: ObjectId;
  brand: string;
  category: string;
  name: string;
  color: number | undefined;
  ingredients: string[];
  product_url: string;
}