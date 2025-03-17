import {useState} from 'react';

const SellerCreateAcct = () => {
    const [phone, setPhone] = useState('');
    const [otp, setOtp] = useState('');
    const [otpSent, setOtpSent] = useState(false);
    const [loading, setLoading] = useState(false);

    //simulate API call to send OTP
    const handleSendOtp = async () => {
        if (!phone.match(/^\d{10,}$/)) {
            alert('Enter a valid phone number');
            return;
        }
        setLoading(true);
        setTimeout(() => {
            setLoading(false);
            setOtpSent(true);
            alert('OTP sent successfully!');
        }, 1000);
    };

    //simulate API call to verify OTP
    const handleVerifyOtp = async () => {
        if (otp.length !== 6) {
            alert('Enter a valid 6-digit OTP');
            return;
        }

        setLoading(true);
        setTimeout(() => {
            setLoading(false);
            alert('Account Created Successfully!');
            //Redirect or store user info after sucess
        }, 1000);
    };

    return (
        <div className='max-w-md-auto mt-10 p-6 border rounded-lg shadow-md'>
            <h2 className='text-2xl font-bold mb-4 text-center'>Create Account</h2>

            {!otpSent ? (
                //Step 1: Enter phone number
                <div>
                    <label className='block mb-2 font-medium'>Phone</label>
                    <input
                      type='tel'
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder='Enter phone number'
                      className='w-full p-2 border rounded-md'
                      disabled={loading}
                    />
                    <button
                       onClick={handleSendOtp}
                       className='mt-3 w-full px-4 py-2 bg-blue-500 text-white rounded-md'
                       disabled={loading}
                    >
                        {loading ? 'Sending...' : 'Send OTP'}
                    </button>
                </div>
            ):(
                //Step 2: Enter OTP
                <div>
                    <label className='block mb-2 font-medium'>OTP</label>
                    <input
                      type='number'
                      value={otp}
                      onChange={(e) => setOtp(e.target.value)}
                      placeholder='Enter OTP'
                      className='w-full p-2 border rounded-md'
                      disabled={loading}
                    />
                    <button
                       onClick={handleVerifyOtp}
                       className='mt-3 w-full px-4 py-2 bg-blue-500 text-white rounded-md'
                       disabled={loading}
                    >
                        {loading ? 'Verifying...' : 'Verify OTP'}
                    </button>
                </div>
            )
            }
        </div>
    );
};

export default SellerCreateAcct;