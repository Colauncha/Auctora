import Input from "../../Components/auth/Input";
import BreadCrumb from "../../Components/Breadcrumbs";
import Button from "../../Components/Button";
import { useState } from "react";

const BankVerification = () => {
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
                Bank Information
              </strong>
              <div className="grid lg:grid-cols-2 gap-2 lg:gap-10 lg:place-items-center ">
                <Input
                  placeholder={`Name`}
                  id={`Name`}
                  type={`text`}
                  htmlFor={`Name`}
                  className={`w-full lg:w-[400px]`}
                />
                <Input
                  placeholder={`Account Number`}
                  id={`account-number`}
                  type={`number`}
                  htmlFor={`account-number`}
                  className={`w-full lg:w-[400px]`}
                />
              </div>
              <div className="grid lg:grid-cols-2 mt-4 gap-10 lg:place-items-center">
                {/* Bank */}
                <select
                  name="area"
                  value={formData.area}
                  onChange={handleChange}
                  className="w-full lg:w-[400px] p-2 border rounded bg-gray-100"
                >
                  <option value="">Bank</option>
                  <option value="Ikeja">First Bank</option>
                  <option value="Lekki">Guarantee Trust Bank</option>
                  <option value="Lekki">UBA</option>
                </select>
              </div>
              <div className="grid lg:grid-cols-2 gap-8  lg:place-items-center"></div>
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

export default BankVerification;
