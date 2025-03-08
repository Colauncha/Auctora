import PropTypes from 'prop-types';


const Avatar = ({ imageUrl, username }) => {

  return (
    <>
      {imageUrl ? (
        <img className="flex h-[150px] w-[150px] rounded-full" src={imageUrl} alt="avatar" />
        ) : (
          <div className="flex items-center justify-center h-[150px] w-[150px] bg-[#9F3247] text-white font-bold text-[3rem] rounded-full">
            {username && username[0].toUpperCase()}
          </div>
        )
      }
    </>
  )

}

Avatar.propTypes = {
  imageUrl: PropTypes.string,
  username: PropTypes.string
}

export default Avatar;