import React from 'react'
import BreadCrumb from '../../Components/Breadcrumbs'
import ItemReview from "../../Components/ItemReview"
import ItemDetail from "../../Components/ItemDetail"
import ItemImage from "../../Components/ItemImage"
import ItemBid from "../../Components/ItemBid"
import { productListArr } from '../../Constants'
const Detail = () => {
  return (
    <div className='formatter'>
        <BreadCrumb/>

        <div className="flex flex-col">
        {productListArr.map((item, idx) => {
          return (
            <div>
            <div className="flex justify-between" key={idx}>
                <ItemImage img={item.imgUrl}/>
                <ItemBid/>
            </div>
            <ItemDetail/>
            <ItemReview/>
        </div>
          );
        })}
           
        </div>
    </div>
  )
}

export default Detail