import BreadCrumb from "../../Components/Breadcrumbs";
import Input from "../../Components/auth/Input";
import Button from "../../Components/Button";
import { useState } from "react";

const AddressVerification = () => {
  const [formData, setFormData] = useState({
    country: "Nigeria",
    state: "",
    area: "",
    address: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
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
                Address Information
              </strong>
              <div className="grid lg:grid-cols-2 gap-2 lg:gap-10 lg:place-items-center ">
                {/* Country Select */}
                <select
                  name="country"
                  value={formData.country}
                  onChange={handleChange}
                  className="w-full p-2 border rounded bg-gray-100"
                  disabled
                >
                  <option value="Nigeria">Nigeria</option>
                </select>
                {/* State selection */}

                <select
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  className="w-full p-2 border rounded bg-gray-100"
                >
                  <option value="">Select State</option>
                  <option value="Lagos">Lagos</option>
                  <option value="Abuja">Abuja</option>
                </select>
              </div>
              <div className="grid lg:grid-cols-2 gap-10 lg:place-items-center">
                {/* Area */}
                <select
                  name="area"
                  value={formData.area}
                  onChange={handleChange}
                  className="w-full p-2 border rounded bg-gray-100"
                >
                  <option value="">Select Area</option>
                  <option value="Ikeja">Ikeja</option>
                  <option value="Lekki">Lekki</option>
                </select>
              </div>
              <div className="grid lg:place-items-center">
                {/* Text-Area */}
                <textarea
                  name="address"
                  value={formData.address}
                  onChange={handleChange}
                  className="w-full p-2 border rounded mt-4 bg-gray-100"
                  placeholder="Enter complete address here"
                ></textarea>
              </div>
              <div className="grid lg:grid-cols-2 gap-8 lg:place-items-center"></div>
              <div className="formatter w-full lg:w-[400px]">
                <Button
                  label={`Next`}
                  className={`mt-5 rounded-md w-44 hover:bg-[#b02b46]`}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default AddressVerification;
