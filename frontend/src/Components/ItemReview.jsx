import React from 'react'
import Button from './Button'
import Star from './Star'

const ItemReview = ({reviewText, reviewerName, reviewImg}) => {
  return (
    <div className='flex flex-col lg:flex-row border-[1px] rounded-md my-5 p-2 flex gap-6'>
      <div className='flex flex-col'>
      <div className='flex gap-4 items-center'>
          <img src={reviewImg} className='w-10 h-10 rounded-full border-[1px]' />
          <div className='flex flex-col text-sm'>
            <span className='font-bold text-[12px]'>{reviewerName}</span>
            <Star/>
          </div>
      </div>
      <p className='text-[12px] '>{reviewText }</p>
      </div>
     <div className='flex flex-col gap-1 justify-center'>
      <Button label={`Other products`} className={`rounded-md text-sm`}/>
      <Button label={`Contact`}  className={`rounded-md text-sm`}/>
     </div>
    </div>
  )
}

export default ItemReview