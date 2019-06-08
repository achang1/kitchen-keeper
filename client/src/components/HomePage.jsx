import React, {Component, Fragment} from 'react';
import {connect} from "react-redux";
import { initializeHomePage } from '../actions';

class HomePage extends Component {
    componentDidMount() {
        this.props.onLoad();
    }

    render() {
        return (
            <Fragment>
                <ul>
                    {this.props.allUsers.map(user => {
                        return (
                            <li key={user.id}>
                                {user.userName}
                            </li>
                        )
                    })}
                </ul>
                <ul>
                    {this.props.allStorages.map(storage => {
                        return (
                            <li key={storage.id}>
                                {storage.storageType}
                            </li>
                        )
                    })}
                </ul>
            </Fragment>
        )
    }
}

const mapStateToProps = state => {
    console.log(state);
    return {
      allUsers: state.allUsers,
      allStorages: state.allStorages
    }
};

function mapDispatchToProps(dispatch) {
    return {
        onLoad: () => initializeHomePage(dispatch)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(HomePage);