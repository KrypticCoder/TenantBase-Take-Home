import React from 'react';
import PropTypes from 'prop-types';
import MenuItem from '../MenuItem';

Menu.defaultProps = {
    items: []
}

Menu.propTypes = {
    items: PropTypes.array
}

export default function Menu({items}) {
    return (
        <div className='menu container'>
            {items.map((item, i) => <MenuItem key={i} item={item} />)}
        </div>
    );
}
