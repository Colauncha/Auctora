import { useLocation } from "react-router-dom";

const BreadCrumb = () => {
  const location = useLocation();
  const pathnames = location.pathname.split("/").filter((x) => x);

  return (
    <div className="breadcrumb">
      <div className="breadcrumb_item">
        <a href="/">Home</a>
        {pathnames.map((name, index) => {
          // Generate the route path for each breadcrumb
          const routeTo = `/${pathnames.slice(0, index + 1).join("/")}`;
          const isLast = index === pathnames.length - 1;
          return isLast ? (
            <span key={name}>&nbsp;&gt;&nbsp;{name}</span>
          ) : (
            <span key={name}>
              &nbsp;&gt;&nbsp;<a href={routeTo}>{name}</a>
            </span>
          );
        })}
      </div>
    </div>
  );
};

export default BreadCrumb;
