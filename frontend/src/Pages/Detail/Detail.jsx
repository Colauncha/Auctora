// import React from 'react'
import { useParams, useNavigate } from "react-router-dom";
import BreadCrumb from '../../Components/Breadcrumbs'
import ItemReview from "../../Components/ItemReview"
import ItemDetail from "../../Components/ItemDetail"
import ItemImage from "../../Components/ItemImage"
import ItemBid from "../../Components/ItemBid"
import { productListArr } from '../../Constants'
import { FaExclamationTriangle } from 'react-icons/fa';
const DetailPage = () => {
const { slug } = useParams();
  const navigate = useNavigate();
  const product = productListArr.find((item) => item.slug ===(slug));
  console.log(product);
  
  if (!product) {
    return <div className=" formatter p-4 border-[1px] rounded-lg h-screen  text-3xl text-red-500 flex mr-4 items-center justify-center"><FaExclamationTriangle/> Item not found</div>;
  }
  return (
    <div className='formatter'>
        <BreadCrumb/>

        <div className="flex flex-col my-10">
            <div className="flex flex-col lg:flex-row justify-between">
                <ItemImage img={product.imgUrl}/>
                <ItemBid price={product.price} title={product.description.title} bid={product.bidTimes}/>
            </div>
            <ItemDetail desc={product.description.detail} title={product.description.title}/>
            <ItemReview reviewText={product.review.reviewText} reviewImg={product.review.rewiewerImg} reviewerName={product.review.reviewerName}/>
        </div>
    </div>
  )
}

export default DetailPage;