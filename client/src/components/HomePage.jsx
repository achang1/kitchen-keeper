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
                {/* <button
                    onClick={() => this.fetchUsers()}>
                    GET Users
                </button>
                <button
                    onClick={() => this.fetchStorages()}>
                    Get Storages
                </button> */}
            </Fragment>
        )
    }
}

const mapStateToProps = state => {
    console.log(state);
    return {
      allUsers: state.allUsers
    }
};

function mapDispatchToProps(dispatch) {
    return {
        onLoad: () => initializeHomePage(dispatch)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(HomePage);