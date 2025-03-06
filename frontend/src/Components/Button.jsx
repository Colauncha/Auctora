// import React from "react";
import PropTypes from 'prop-types';

const Button = ({ label, className, onClick, icon, iconClassName }) => {
  return (
    <div>
      <button
        className={`bg-[#9F3247] text-white px-4 w-full h-[42px] rounded-[62px] ${className}`}
        onClick={onClick}
      >
        {label}
        {icon ? <img className={iconClassName} src={icon}/> : ""}
      </button>
    </div>
  );
};
Button.propTypes = {
  label: PropTypes.string.isRequired,
  className: PropTypes.string,
  onClick: PropTypes.func,
  icon: PropTypes.string,
  iconClassName: PropTypes.string,
};

export default Button;
