import { useState } from "react";

const Delivery = () => {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [shippingDate, setShippingDate] = useState("");

  const handleOptionChange = (option) => {
    setSelectedOptions((prev) =>
      prev.includes(option) ? prev.filter((item) => item !== option) : [...prev, option]
    );
  };

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
      <h4 className="text-sm font-semibold mb-4">Select delivery options</h4>

      {/* Checkbox Options */}
      <div className="space-y-3 text-xs">
        {["Self pickup", "Online payment", "Courier cash on delivery"].map((option) => (
          <label key={option} className="flex items-center space-x-2 cursor-pointer w-1/3 mt-1 p-2 border border-gray-200 rounded-lg bg-gray-50">
            <input
              type="checkbox"
              checked={selectedOptions.includes(option)}
              onChange={() => handleOptionChange(option)}
              className="w-5 h-5 rounded border-gray-400 text-red-800 focus:ring-red-800"
            />
            <span className="text-gray-700">{option}</span>
          </label>
        ))}
      </div>

      {/* Shipping Time Input */}
      <div className="mt-4">
        <h3 className="text-sm font-medium">Shipping time</h3>
        <input
          type="text"
          name="date"
          placeholder="Specify a date"
          value={shippingDate}
          onChange={(e) => setShippingDate(e.target.value)}
          className="w-full mt-1 px-3 py-2 border bg-gray-50 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-800"
        />
      </div>

      {/* Next Button */}
      <button className="mt-6 w-40 bg-red-800 text-white py-2 rounded-3xl font-medium hover:bg-red-900 transition mx-auto block">
        Next
      </button>
    </div>
  </div>
  );
}

export default Delivery;

