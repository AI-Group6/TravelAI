import React, {useState} from 'react';

const Sidebar = ({ chatHistory, onChatClick }) => {
    const [previousEntries, setPreviousEntries] = useState([
        { title: 'Trip to Paris', date: '2023-09-17', id: 1, chatHistory: 'This is a great place to go!'},
        { title: 'Trip to Thailand', date: '2023-09-17', id: 2, chatHistory: 'I love this place'},
    ])

    return (
        <div>
            <p className="font-josefin text-2xl text-center my-3 font-semibold">
                Previous Planning
            </p>
            <hr className='mb-5'/>
            {(chatHistory || []).map((chat, index) => (
                <div key={index} className='mb-5 cursor-pointer' onClick={() => onChatClick(chat)}>
                    <p className='font-josefin text-xl underline font-medium'>
                        {chat.title} {/* Displaying the user's input */}
                    </p>
                    <p className='font-josefin font-thin'>
                        {chat.date} {/* Displaying the date */}
                    </p>
                </div>
            ))}
        </div>
    );
};

export default Sidebar;