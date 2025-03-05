// import React from "react";
import Button from "../../Components/Button";
import BreadCrumb from "../../Components/Breadcrumbs";
import { useNavigate } from "react-router-dom";

const GetStarted = () => {
  const navigate = useNavigate();
  const handleAddProduct = () => {
    navigate("/add-product");
  };
  return (
    <>
      <div className="formatter">
        <BreadCrumb />
      </div>
      <div className="bg-slate-50 my-10 py-5">
        <div className="formatter">
          <div className=" bg-white py-10 px-5 rounded-md  shadow-md">
            <div className="w-full flex flex-col gap-2">
              <strong className="text-xl lg:text-2xl text-[#9f3247] font-extrabold mb-6">
                Get Started
              </strong>
              <div className="grid place-items-center ">
                <p className="text-sm">Add your first product to sell</p>
                <span>
                  <Button label="Add Product" onClick={handleAddProduct} />
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default GetStarted;
