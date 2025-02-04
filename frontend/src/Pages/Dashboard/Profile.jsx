import BreadCrumb from "../../Components/Breadcrumbs";
import Input from "../../Components/auth/Input";
import Button from "../../Components/Button";
import FileInput from "../../Components/FileInput";

const Profile = () => {
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
                Profile Information
              </strong>
              <div className="grid lg:grid-cols-2 gap-10 lg:place-items-center ">
                <Input
                  title={`Name`}
                  id={`Phone`}
                  type={`phone`}
                  htmlFor={`phone`}
                  className={`w-full lg:w-[400px]`}
                />
                <Input
                  title={`Email`}
                  id={`Phone`}
                  type={`phone`}
                  htmlFor={`phone`}
                  className={`w-full lg:w-[400px]`}
                />
              </div>
              <div className="grid lg:grid-cols-2 gap-10 lg:place-items-center">
                <Input
                  title={`Phone`}
                  id={`Phone`}
                  type={`phone`}
                  htmlFor={`phone`}
                  className={`w-full lg:w-[400px]`}
                />
              </div>

              <div className="grid lg:grid-cols-2 mt-4 gap-8 lg:place-items-center">
                <FileInput text={`Upload ID Picture Front-view`} />
                <FileInput text={`Upload ID Picture Backt-view`} />
              </div>
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

export default Profile;
