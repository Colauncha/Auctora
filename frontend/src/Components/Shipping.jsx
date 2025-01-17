import React from 'react'
import { delivery, shipping } from '../Constants'

const Shipping = () => {
  return (
    <div className='flex flex-row lg:flex-col items-center justify-center lg:items-start'>
        <div className='border-[1px] w-[50%] lg:w-full h-[130px] lg:h-[100px]'>
          <div className='flex items-center justify-center lg:justify-start gap-3 p-3'>
            <img src={shipping} alt="" />
            <div className='flex flex-col'>
                <h4 className='font-bold'>Shipping</h4>
                <p className='text-[12px]'>N1000 per Order</p>
            </div>
          </div>
        </div>
        <div className='border-[1px] w-[50%] lg:w-full h-[130px] lg:h-[100px]'>
        <div className='flex items-start justify-center gap-3 p-3'>
            <img src={delivery} alt="" />
            <div className='flex flex-col'>
                <h4 className='font-bold'>Delivery</h4>
                <p className='text-[12px]'>Estimated between Thu, Jan 4 and Fri, Jan 12</p>
            </div>
          </div>                                                  
        </div>
    </div>
  )
}

export default Shipping