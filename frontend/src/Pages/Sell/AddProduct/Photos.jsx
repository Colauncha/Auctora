import { useState } from "react";
import { FiUpload, FiTrash } from "react-icons/fi";

const Photo = () => {
  const [images, setImages] = useState([
    // {
    //   name: "",
    //   size: ,
      
    // },
    // {
    //   name: "image2.jpg",
    //   size: ,
      
    // },
    // {
    //   name: "",
    //   size: ,
    // },
    // {
    //   name: "",
    //   size: ,
    // }
  ]);
  const maxSize = 25 * 1024 * 1024; // 25MB limit
  const maxImages = 10;

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.size <= maxSize && images.length < maxImages) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImages([...images, { name: file.name, size: file.size, url: reader.result }]);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDelete = (index) => {
    setImages(images.filter((_, i) => i !== index));
  };

  return (
    <div className="max-w-3xl mx-auto p-5 bg-gray-100 rounded-md">
      <h2 className="text-xl font-semibold mb-4">Add Product Photos (Max 10)</h2>

      <div className="flex flex-wrap gap-4">
        <label className="w-28 h-28 border-2 border-dashed border-gray-200 flex flex-col items-center justify-center text-gray-500 cursor-pointer">
          <FiUpload size={24} />
          <span className="text-sm">Upload a photo</span>
          <input type="file" accept="image/*" className="hidden" onChange={handleUpload} />
        </label>

        {images.map((img, index) => (
          <div key={index} className="relative w-28 h-28 border bg-white p-2">
            <img src={img.url} alt={img.name} className="w-full h-full object-cover rounded" />
            <button
              onClick={() => handleDelete(index)}
              className="absolute top-1 right-1 bg-red-800 text-white p-1 rounded-full"
            >
              <FiTrash size={14} />
            </button>
            <p className="text-xs mt-1 text-center">{(img.size / (1024 * 1024)).toFixed(2)} MB</p>
          </div>
        ))}
      </div>

      <button className="mt-6 w-40 bg-red-800 text-white py-2 rounded- font-medium hover:bg-red-900 transition mx-auto block">
        Next
      </button>
    </div>
  );
};

export default Photo;
