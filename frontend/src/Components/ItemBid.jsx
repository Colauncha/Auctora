import { useState } from 'react'
import Stopwatch from './Stopwatch'
import Modal from './Modal'
import Button from './Button'
import BidModal from './BidModal'
import { FaHeart } from 'react-icons/fa'
import Shipping from './Shipping'

const ItemBid = ({title,bid, price, desc}) => {
  const [modalOpen, setModalOpen] = useState(false);
    const openModal = () => setModalOpen(true);
    const closeModal = () => setModalOpen(false);
  return (
    <div className='w-[400px] h-[450px]  rounded-md flex flex-col gap-4 p-10'>
      <div className='text-[15px] font-bold text-[#9f3247]'>
        {title}
      </div>
      <div className='flex text-sm items-end gap-2 md:flex-col md:items-center'>
      <Stopwatch/> Remaining
      </div>
      <div className='flex items-center gap-6'>
        <div className='text-[20px]'>
        ₦{price}
        </div>
       <span className='text-slate-400'>({bid} bids)</span> 
      </div>
      <div>
       { desc}
      </div>
     <div className='flex items-center  gap-4'>
     <Button label={`Bid Now`} onClick={openModal} className={`rounded-md w-[250px]`}/>
     <Button label={<FaHeart color='#9f3247'/>} className={`w-10 rounded-md border-[1px] bg-white`}/>
     <Modal isOpen={modalOpen} onClose={closeModal}>
      <BidModal/>
     </Modal>
     
     </div>
     <div>
      <Shipping/>
     </div>
     
    </div>
  )
}

export default ItemBid