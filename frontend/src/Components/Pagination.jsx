import React from 'react';

const Pagination = ({ totalPages, currentPage, onPageChange }) => {
  const handlePageClick = (page) => {
    if (page >= 1 && page <= totalPages) {
      onPageChange(page);
    }
  };

  const renderPageNumbers = () => {
    const pages = [];

    // Add the first page
    if (currentPage > 3) {
      pages.push(1);
      if (currentPage > 4) pages.push('...');
    }

    // Add the current page and its neighbors
    for (let i = Math.max(1, currentPage - 1); i <= Math.min(totalPages, currentPage + 1); i++) {
      pages.push(i);
    }

    // Add the last page
    if (currentPage < totalPages - 2) {
      if (currentPage < totalPages - 3) pages.push('...');
      pages.push(totalPages);
    }

    return pages;
  };

  return (
    <div className="flex items-center justify-center space-x-2 mt-4">
      {/* Previous Button */}
      <button
        onClick={() => handlePageClick(currentPage - 1)}
        disabled={currentPage === 1}
        className={`flex items-center justify-center px-4 py-2 border rounded-md text-[#7B2334] border-[#7B2334] ${currentPage === 1
          ? 'opacity-50 cursor-not-allowed'
          : 'hover:bg-[#7B2334] hover:text-white'
        }`}
      >
        &larr; Previous
      </button>

      {/* Page Numbers */}
      {renderPageNumbers().map((page, index) =>
        typeof page === 'number' ? (
          <button
            key={index}
            onClick={() => handlePageClick(page)}
            className={`px-4 py-2 rounded-md ${page === currentPage
              ? 'bg-[#7B2334] text-white'
              : 'text-[#7B2334] border border-[#7B2334] hover:bg-[#7B2334] hover:text-white'
            }`}
          >
            {page}
          </button>
        ) : (
          <span key={index} className="px-4 py-2 text-pink-400">...</span>
        )
      )}

      {/* Next Button */}
      <button
        onClick={() => handlePageClick(currentPage + 1)}
        disabled={currentPage === totalPages}
        className={`flex items-center justify-center px-4 py-2 border rounded-md text-[#7B2334] border-[#7B2334] ${currentPage === totalPages
          ? 'opacity-50 cursor-not-allowed'
          : 'hover:bg-[#7B2334] hover:text-white'
        }`}
      >
        Next &rarr;
      </button>
    </div>
  );
};

export default Pagination;
