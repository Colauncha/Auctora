import {useState} from "react";


const Description = () => {
    const [product, setProduct] = useState({
        name: "",
        description: "",
        availability: "",
        dimensions: {length: 0, width: 0, height: 0},
        price: "",
    });

    const handleChange = (e) => {
        const {name, value} = e.target;
        setProduct({...product, [name]: value});
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(product);
    };

     {/* <h2 className="text-xl font-bold">Sell Add Product</h2> */}

    return (
        <div className="bg-gray-200 p-6 rounded-lg shadow-md"> 
        {/* Image and Image name */}
        <div className="flex items-center space-x-4 mb-6">
            <img 
              src="" 
              alt="" 
              className="" 
            />
            <span className="text-lg font-semibold text-gray-800">Description</span>
            <span className="text-lg font-semibold text-gray-800">Categories</span>
            <span className="text-lg font-semibold text-gray-800">Photos</span>
            <span className="text-lg font-semibold text-gray-800">Delivery</span>
            
        </div>

        <div className="max-w-7xl mx-auto p-6 bg-white shadow-md rounded-lg">
            <h5 className="text-xl font-semibold mb-3">Fill in the basic information about your item</h5>
            <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-6">

                {/* Left Side - Product name & Description */}
            <div className="flex flex-col space-y-4">
                {/* Product Name */}
                <div>
                    <label className="block text-black font-semibold">Product name</label>
                <input 
                   type="text"
                   name="name"
                   placeholder="Graphic card GIGABYTE GeForce RTX 3050"
                   value={product.name}
                   onChange={handleChange}
                   className="w-full mt-1 p-2 border border-gray-200 rounded-lg bg-gray-100"
                   maxLength={60} 
                />
                 <p className="text-sm text-gray-500 mt-1">{product.name.length}/60</p>
                </div>

                {/* Description */}
                <div>
                <label className="block text-black font-semibold">Description</label>
                <textarea
                   name="description"
                   placeholder="Enter product details..."
                   value={product.description}
                   onChange={handleChange}
                   className="w-full mt-1 p-2 border border-gray-300 rounded-lg bg-gray-100 h-60"
                   maxLength={1200}
                />
                <p className="text-sm text-gray-500 mt-1">{product.description.length}/1200</p>
                </div>

                {/* Next Button */}
                <button type="submit" className="w-1/3 bg-red-800 text-white py-3 rounded-3xl text-sm hover:bg-red-900">
                    Next
                </button>
                </div>


                {/* Right Side - Units, Dimensions, & Price */}
              <div className="flex flex-col space-y-4"> 
                {/* Availability */}
                <div>
                <label className="block text-black font-semibold">Number of units available</label>
                <input 
                   type="number"
                   name="availability"
                   placeholder="Availability"
                   value={product.availability}
                   onChange={handleChange}
                   className="w-3/4 mt-1 p-2 border border-gray-200 rounded-lg bg-gray-100"
                />
                </div>

                {/* Dimension */}
                <div>
                <label className="block text-black font-semibold">Dimensions (optional)</label>
                <div className="flex flex-col space-y-2 ">
                <div className="flex items-center gap-2">
                <label>Length [mm]</label>
                <input
                    type="number"
                    name="length"
                    placeholder="0"
                    value={product.length}
                    onChange={handleChange}
                    className="w-12 p-2 border border-gray-300 rounded-md text-gray-700"
                />
                </div>
                <div className="flex items-center gap-2">
                <label>Width [mm]</label>
                <input
                    type="number"
                    name="width"
                    placeholder="0"
                    value={product.length}
                    onChange={handleChange}
                    className="w-12 p-2 border border-gray-300 rounded-md text-gray-700"
                />
                </div>
                <div className="flex items-center gap-2">
                <label>Height [mm]</label>
                <input
                    type="number"
                    name="height"
                    placeholder="0"
                    value={product.length}
                    onChange={handleChange}
                    className="w-12 p-2 border border-gray-300 rounded-md text-gray-700"
                />
                </div>
                </div> 
                </div>

                {/* Price */}
                <div>
                <label className="block text-black font-semibold">Initial price</label>
                <input 
                   type="number"
                   name="price"
                   placeholder="Product price"
                   value={product.price}
                   onChange={handleChange}
                   className="w-2/4 mt-1 p-2 border border-gray-200 rounded-lg bg-gray-100"
                />
                </div>

                </div> 
            </form>
        </div> 
        </div>
    );
};

export default Description;
