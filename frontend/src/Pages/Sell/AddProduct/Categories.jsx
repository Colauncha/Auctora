import {useState} from "react";

const categories = [
  {
    title: "",
    subcategories: [
      {
        title: "Phones and axesories",
        items: ["Smartphones", "Smartwatches", "Tablets", "Axesories GSM", "Cases and covers"],
      },
      {
        title: "Computer",
        items: ["Laptops", "Laptop components", "Desktop Computers", "Computer components", "Printers and scanners"],
      },
      {
        title: "TVs and axesories",
        items: ["TVs", "Projectors", "Headphones", "Audio for home", "Home cinema"],
      },
      {
        title: "Consoles and slot machines",
        items: ["Consoles PlayStation 5", "Consoles Xbox Series X/S", "Consoles PlayStation 4", "Consoles Xbox One", "Consoles Nintendo Switch"],
      },
    ],
  },

{
  title: "",
  subcategories: [
    {
      title: "Minor",
     items: ["Kitchen, cooking", "Hygiene and care", "For home", "Vacuum cleaners"],
   },
   {
     title: "Appliances",
     items: ["Fridges", "Washing machines", "Clothes dryers", "Free-standing kitchens"],
   },
   {
    title: "Built-in appliances",
     items: ["Hotplates", "Built-in ovens", "Built-in dishwashers", "Hoods"],
  },
   {
    title: "Photography",
     items: ["Digital cameras", "Lenses", "Photo axesories", "Instant cameras (Instax, Polaroid)"],
   },
  ],
},
];


export default function CategorySelection() {
  const [selectedCategories, setSelectedCategories] = useState([]);

  const handleCategorySelect = (category) => {
    if (selectedCategories.includes(category)) {
      setSelectedCategories(selectedCategories.filter((item) => item !== category));
    } else if (selectedCategories.length < 3) {
      setSelectedCategories([...selectedCategories, category]);
    }
  };

  return (
    <div className="max-w-6xl mx-auto bg-white shadow-md rounded-lg p-6">
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

      <h2 className="text-lg font-semibold mb-4">Select the category your goods belong to (max. 3)</h2>

      {/* Top Section */}
      <div className="flex flex-wrap gap-x-6 gap-y-4 mb-6">
        {categories.slice(0, 1).map((category, index) => (
          <div key={index} className="flex-1 min-w-[250px] grid grid-cols-5 gap-3 text-center text-gray-700">
            <h3 className="font-bold mb-4 text-lg text-gray-800">{category.title}</h3>
            {category.subcategories.map((sub, idx) => (
              <div key={idx} className=" mt-6 grid grid-cols-1">
                <h4 className="text-md font-medium grid grid-cols-1">{sub.title}</h4>
                <div className="flex flex-col gap-1">
                  {sub.items.map((item, id) => (
                    <label key={id} className="flex items-center space-x-3 cursor-pointer">      
                   <input
                     type="checkbox"
                     checked={selectedCategories.includes(item)}
                     onChange={() => handleCategorySelect(item)}
                     className="w-6 h-6 appearance-none border-2 border-gray-400 rounded-md checked:bg-red-800 checked:border-red-800"
                   />
                      <span>{item}</span>
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* Bottom Section */}
      <div className="flex flex-wrap gap-x-6 gap-y-4 mt-6">
        {categories.slice(1).map((category, index) => (
          <div key={index} className="flex-1 min-w-[250px] grid grid-cols-5 gap-3 text-center text-gray-700">
            <h3 className="font-bold mb-4 text-lg text-gray-800">{category.title}</h3>
            {category.subcategories.map((sub, idx) => (
              <div key={idx} className="mt-2">
                <h4 className="text-md font-medium grid grid-cols-1">{sub.title}</h4>
                <div className="flex flex-col gap-1">
                  {sub.items.map((item, id) => (
                    <label key={id} className="flex items-center space-x-3 cursor-pointer">
                      <input
                     type="checkbox"
                     checked={selectedCategories.includes(item)}
                     onChange={() => handleCategorySelect(item)}
                     className="w-6 h-6 appearance-none border-2 border-gray-400 rounded-md checked:bg-red-800 checked:border-red-800"
                   />
                      <span>{item}</span>
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>

      <div className="mt-4">
        <h3 className="text-sm font-semibold">Selected categories:</h3>
        <div className="flex flex-wrap gap-2 mt-2 font-semibold">
          {selectedCategories.map((category, index) => (
            <span key={index} className="bg-red-800 text-white text-sm px-2 py-1 rounded">
              {category}
            </span>
          ))}
        </div>
      </div>

      <button className="mt-6 w-40 bg-red-800 text-white py-2 rounded-3xl font-medium hover:bg-red-900 transition mx-auto block">
        Next
      </button>
    </div>
  );
}