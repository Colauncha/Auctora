import React from 'react'

const ItemDetail = ({desc, title}) => {
  return (
    <div>
      <h3 className='text-[#9f3247] font-bold my-5 text-xl '>About {title}</h3>
      <p className='text-[13px]'>{desc}</p>
    </div>
  )
}

export default ItemDetail