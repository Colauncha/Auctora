import { Link } from "react-router-dom";
import Cta from "./Cta";
import { facebook, github, instaggram, logo, twitter } from "../../Constants";

const footerArr = [
  {
    heading: "Company",
    links: [
      { name: "About", url: "/about" },
      { name: "Features", url: "/features" },
      { name: "Works", url: "/works" },
      { name: "Career", url: "/career" },
    ],
  },
  {
    heading: "Help",
    links: [
      { name: "Customer Support", url: "/customer-support" },
      { name: "Delivery Details", url: "/delivery-details" },
      { name: "Terms & Conditions", url: "/terms" },
      { name: "Privacy Policy", url: "/privacy" },
    ],
  },
  {
    heading: "Contact",
    links: [
      { name: "Account", url: "/account" },
      { name: "Manage Deliveries", url: "/delivery" },
      { name: "Orders", url: "/orders" },
      { name: "Payments", url: "/payments" },
    ],
  },
];

const Footer = () => {
  return (
    <div className="bg-[#F0F0F0] min-h-screen w-full lg:h-[500px]">
      <Cta />
      <footer className="formatter flex flex-col text-[#9F3247]">
        <div className="py-10 flex flex-col gap-6 md:flex-row">
          <div className="flex flex-col w-full gap-8 md:w-[450px] ">
            <img src={logo} alt="" className="w-28 h-10 lg:w-40 lg:h-12" />
            <p>
              Join online auctions and find unique items to buy and sell with
              excitement!
            </p>
            <div className="flex gap-4">
              <img src={facebook} alt="" />
              <img src={twitter} alt="" />
              <img src={instaggram} alt="" />
              <img src={github} alt="" />
            </div>
          </div>
          <div className="flex flex-col md:flex-row justify-between md:w-full flex-1">
            <div className="flex flex-col gap-5 lg:flex-row justify-between flex-1">
              {footerArr.map((section, index) => (
                <div key={index}>
                  <h4 className="text-lg font-bold mb-4">{section.heading}</h4>
                  <ul className="flex flex-1 flex-col gap-5">
                    {section.links.map((link, idx) => (
                      <li key={idx}>
                        <a
                          href={link.url}
                          className="text-[#9f3247] hover:underline underline-offset-2"
                        >
                          {link.name}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="mt-6 border-t-[1px] pt-5 text-center md:text-start">
          Auctora © 2024, All Rights Reserved
        </div>
      </footer>
    </div>
  );
};

export default Footer;
