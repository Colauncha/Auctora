import {} from "react";

const products = [
  { id: 1, name: " ", price: " ", bids: 3, image: " " },
  { id: 2, name: " ", price: " ", bid: 3, image: " " },
  { id: 3, name: " ", price: " ", bids: 3, image: " " }
];

const Products = () => {
  return (
    <div className="bg-gray-200 p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-red-800">Your Products</h2>
      <div className="mt-4 grid grid-cols-5 gap-6 max-w-7xl mx-auto p-6 bg-white shadow-md rounded-lg">
        {products.map((product) => (
          <div key={product.id} className="border p-4 bg-gray-200 rounded-lg shadow-md">
            <img src={product.image} alt={product.name} className="w-full h-32 object-cover rounded-md" />
          </div>
        ))}
        {/* <div className="flex flex-col items-center justify-center border p-4 bg-gray-200 rounded-lg shadow-md"> 
        <p className="mt-2 text-sm font-semibold">{products.name}</p>
        <p className="text-gray-600">{products.price} ({products.bids} bids)</p>
        </div> */}
        <div className="flex items-center justify-center border p-4 bg-red-50 rounded-lg shadow-md cursor-pointer">
          <span className="text-5xl font-normal text-red-700">+</span>
        </div>
      </div>
    </div>
  );
};

export default Products;
