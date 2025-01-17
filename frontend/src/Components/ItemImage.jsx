import React from 'react'

const ItemImage = ({img}) => {
  return (
    <div className='w-full border-[1px] rounded-md flex items-center lg:items-start justify-center lg:justify-start'>
      <div className=' h-72 flex justify-center flex-col gap-2'>
        <img src={img} alt="" className='w-12 h-12 lg:w-16 lg:h-16 border-[1px] p-2 rounded-md' />
        <img src={img} alt="" className='w-12 h-12 lg:w-16 lg:h-16  border-[1px] p-2 rounded-md ' />
        <img src={img} alt="" className='w-12 h-12 lg:w-16 lg:h-16 border-[1px] p-2 rounded-md ' />
        <img src={img} alt="" className='w-12 h-12 lg:w-16 lg:h-16  border-[1px] p-2 rounded-md ' />
       
      </div>
      <img src={img} className='h-[300px] lg:h-[490px]' />
    </div>
  )
}

export default ItemImage