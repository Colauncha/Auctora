import BreadCrumb from "../../Components/Breadcrumbs";
import Button from "../../Components/Button";
import Input from "../../Components/auth/Input";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Otp = () => {
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const generateOtp = () => {
    console.log("Generating OTP...");
  };
  const verify = () => {
    try {
      setLoading(true);
      console.log("Verifying...");
    } catch (error) {
      console.error("Error during verification", error);
    } finally {
      setLoading(false);
      console.log("Verification in progress...");
      navigate("/profile");
    }
  };
  return (
    <>
      <div className="formatter">
        <BreadCrumb />
      </div>
      <div className="bg-slate-100 my-10 py-5">
        <div className="formatter">
          <div className=" bg-white p-5 flex justify-center items-center rounded-md">
            <fieldset className="flex flex-col gap-3 w-full lg:w-[300px]">
              <div className="flex flex-col gap-4 mb-10">
                <legend className="text-[30px] font-[700] text-[#9f3247]">
                  <h2>Verify OTP</h2>
                </legend>
                <div>
                  <Input
                    title={`Phone`}
                    id={`Phone`}
                    type={`phone`}
                    htmlFor={`phone`}
                    className={`w-full lg:w-[400px]`}
                  />
                  <div className="flex justify-end">
                    <Button
                      label={`OTP`}
                      className={`bg-transparent text-[#b02b46] font-bold mt-0`}
                      onClick={generateOtp}
                    />
                  </div>
                </div>

                <div className="flex  flex-col gap-1 justify-start">
                  <strong className="text-[#b02b46]">OTP</strong>
                  <div className="flex  gap-2 justify-start">
                    <Input
                      id={`Phone`}
                      type={`phone`}
                      htmlFor={`phone`}
                      className={`w-[40px]`}
                    />
                    <Input
                      id={`Phone`}
                      type={`phone`}
                      htmlFor={`phone`}
                      className={`w-[40px]`}
                    />
                    <Input
                      id={`Phone`}
                      type={`phone`}
                      htmlFor={`phone`}
                      className={`w-[40px]`}
                    />
                    <Input
                      id={`Phone`}
                      type={`phone`}
                      htmlFor={`phone`}
                      className={`w-[40px]`}
                    />
                  </div>
                  <small className="text-slate-400">
                    The code will be sent via sms
                  </small>
                </div>
                <Button
                  label={`Verify`}
                  onClick={verify}
                  className={`hover:bg-[#de506d] w-[500px]`}
                  loading={loading ? "Verifying..." : ""}
                />
              </div>
            </fieldset>
          </div>
        </div>
      </div>
    </>
  );
};

export default Otp;
