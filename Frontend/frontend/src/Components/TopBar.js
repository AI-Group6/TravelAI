import React, { useState } from 'react';
import { Icon } from '@iconify/react';
import {createNewUser} from "../Routes";

const TopBar = () => {

  const [showLogin, setShowLogin] = useState(false);
  const [showNewUser, setShowNewUser] = useState(false); // State to manage new user form visibility
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState(''); // State for confirm password
  const [error, setError] = useState('');

  const toggleLoginPopup = () => {
    setShowLogin(!showLogin);
  };

  const toggleNewUserPopup = () => {
    setShowNewUser(!showNewUser);
    setShowLogin(false); // Hide login form if new user form is toggled
  };

  const handleConfirmPasswordChange = (e) => {
    setConfirmPassword(e.target.value);
  };

  const handleSubmitNewUser = (e) => {
    e.preventDefault();
    
    // Reset error
    setError('');

    // Check if password and confirm password match
    if (password !== confirmPassword) {
        setError('Passwords do not match.');
        return;
    }

    // Proceed with registration logic

    // Here you can call your API to register the user
  };

  //Login info
  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };


  return (
    <div className="w-full h-16 bg-[#563635] flex items-center justify-between px-4 text-white drop-shadow-md">
      <h1 className="text-xl font-bold">AI Travel Assistant</h1>
      <div className="flex items-center space-x-4">
        <Icon icon="iconamoon:profile-circle-fill" onClick={toggleLoginPopup} className="w-12 h-12 hover:text-[#4e2c20] transition duration-200 cursor-pointer"/>
      </div>

      {/* Conditional Rendering for the Login Popup */}
      {showLogin && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 w-screen h-screen">
          <div className="bg-white p-8 rounded shadow-lg w-96">
            {/* Login Title */}
            <h2 className="text-2xl mb-6 font-bold text-gray-800">Login</h2>
            
            {/* Login Form */}
            <form>
              <div className="mb-4">
                <label className="block text-gray-700 mb-2">Username</label>
                <input
                  type="text"
                  value={username} // Control the input value
                  onChange={handleUsernameChange} // Update state on change
                  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-[#4e2c20] text-black"
                  placeholder="Enter your username"
                />
              </div>

              <div className="mb-6">
                <label className="block text-gray-700 mb-2">Password</label>
                <input
                  type="password"
                  value={password} // Control the input value
                  onChange={handlePasswordChange} // Update state on change
                  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-[#4e2c20] text-black"
                  placeholder="Enter your password"
                />
              </div>

              <button
                type="submit"
                className="bg-[#4e2c20] text-white px-4 py-2 rounded w-full hover:bg-[#6a4532]"
              >
                Login
              </button>
            </form>

            {/* New User Button */}
            <button
              onClick={toggleNewUserPopup}
              className="mt-4 text-blue-600 underline block text-center"
            >
              New User? Register Here
            </button>

            {/* Close Button */}
            <button
              onClick={toggleLoginPopup}
              className="mt-4 text-red-600 underline block text-center"
            >
              Close
            </button>
          </div>
        </div>
      )}
      {/* Conditional Rendering for the New User Popup */}
      {/* Conditional Rendering for the New User Popup */}
      {showNewUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 w-screen h-screen">
          <div className="bg-white p-8 rounded shadow-lg w-96">
            <h2 className="text-2xl mb-6 font-bold text-gray-800">New User Registration</h2>
            <form onSubmit={handleSubmitNewUser}>
              <div className="mb-4">
                <label className="block text-gray-700 mb-2">Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={handleUsernameChange}
                  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-[#4e2c20] text-black"
                  placeholder="Enter your username"
                />
              </div>

              <div className="mb-4">
                <label className="block text-gray-700 mb-2">Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={handlePasswordChange}
                  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-[#4e2c20] text-black"
                  placeholder="Enter your password"
                />
              </div>

              <div className="mb-6">
                <label className="block text-gray-700 mb-2">Confirm Password</label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={handleConfirmPasswordChange}
                  className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-[#4e2c20] text-black"
                  placeholder="Confirm your password"
                />
              </div>

              {/* Display error message */}
              {error && <p className="text-red-500 mb-4">{error}</p>}

              <button
                type="submit"
                className="bg-[#4e2c20] text-white px-4 py-2 rounded w-full hover:bg-[#6a4532]"
              >
                Register
              </button>

              <button
                onClick={toggleNewUserPopup}
                className="mt-4 text-red-600 underline block text-center"
              >
                Close
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};



export default TopBar;