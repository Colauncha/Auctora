import { FaSpinner } from "react-icons/fa";
import BreadCrumb from "../../Components/Breadcrumbs";

const VerificationLoading = () => {
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
                Verification
              </strong>
              <div className="grid place-items-center ">
                <p className="text-sm animate-pulse">
                  Please wait for your confirmation mail.
                </p>
                <span>
                  <FaSpinner className="animate-spin text-4xl text-[#9f3247]" />
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default VerificationLoading;
