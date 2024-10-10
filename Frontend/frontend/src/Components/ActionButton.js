// components/ActionButton.js
import React from 'react';

const ActionButton = ({ label, icon, bgColor }) => {
  const [firstWord, secondWord] = label.split(" ");
  return (
    <div className={`h-48 w-2/4 flex flex-col items-center justify-center p-4 ${bgColor} text-[#563635] border border-[#563635] border-2 rounded-md hover:opacity-90 cursor-pointer`}>
      <img src={icon} alt={label} className="h-8 w-8 mb-auto ml-auto"/>
      <div className="w-full text-left"> {/* Added a div to wrap the text */}
        <p className="font-medium whitespace-pre-line">
        {firstWord} <span className="font-bold">{secondWord}</span>
        </p>
      </div>
    </div>
  );
};

export default ActionButton;