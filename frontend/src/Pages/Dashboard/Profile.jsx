import React from "react";
import BreadCrumb from "../../Components/Breadcrumbs";
import Input from "../../Components/auth/Input";
import Button from "../../Components/Button";

const Profile = () => {
  return (
    <>
      <div className="formatter">
        <BreadCrumb />
      </div>
      <div className="bg-slate-100 my-10 py-5">
        <div className="formatter">
          <div className=" bg-white py-10 px-5 rounded-md flex flex-col gap-2">
            <strong>Profile Information</strong>
            <div className="grid lg:grid-cols-2 gap-10 place-items-center">
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
            <div className="grid lg:grid-cols-2 gap-10 place-items-center">
              <Input
                title={`Phone`}
                id={`Phone`}
                type={`phone`}
                htmlFor={`phone`}
                className={`w-full lg:w-[400px]`}
              />
            </div>
            <div className="grid lg:grid-cols-2 gap-10 place-items-center">
              <Input
                title={`Phone`}
                id={`Phone`}
                type={`phone`}
                htmlFor={`phone`}
                className={`w-full lg:w-[400px]`}
              />
              <Input
                title={`Phone`}
                id={`Phone`}
                type={`phone`}
                htmlFor={`phone`}
                className={`w-full lg:w-[400px]`}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Profile;
