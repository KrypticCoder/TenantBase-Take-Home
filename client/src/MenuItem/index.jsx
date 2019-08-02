import React, { useState } from 'react';
import PropTypes from 'prop-types';

import './menuItem.scss';

MenuItem.propTypes = {
    items: PropTypes.node.isRequired
}

export default function MenuItem({item}) {
    const { key, value } = item;
    const [visible, setVisible] = useState(false);

    const toggleVisibility = () => {
        setVisible(!visible);
    };

    return (
        <div className='menu-item row' onClick={toggleVisibility}>
            <div className='col-md-12 text-center'>
                <div className='menu-item__key'>{key}</div>
                {visible && (
                    <div className='menu-item__value'>{value}</div> 
                )}
            </div>
        </div>
    );
}
