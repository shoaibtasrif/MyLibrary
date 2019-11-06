import React from 'react';

class Header extends React.Component {
    constructor(props) {
        document.write(" construcrtor ");
        super(props);
        this.state = { favoritecolor: "red", favbook: "nonte" };
    }

    static getDerivedStateFromProps(props, state) {
        //document.write(" getDeSt ");
        return { favoritecolor: props.favcol };
    }

    componentDidMount() {
        document.write("com did mount ");
        this.setState({ favoritecolor: " timedOut " });
    }

    changeColor = () => {
        //document.write("click");
        this.setState({ favoritecolor: "changed" });
        this.setState({ favbook: "fonte" });
        //document.write("\n" + this.state.favoritecolor + "\n");
    }

    render() {
        //document.write(" render" + this.state.favoritecolor + " ");
        return (
            <div>
                <h1>My Favorite Color is {this.state.favoritecolor} {this.state.favbook}</h1>
                <button type="button" onClick={this.changeColor}>Change Color</button>
            </div>
        );
    }
}

// once the getDerivedStateFromProps is declared it will be executed everytime
// before rendering . it may be rendered due to any change to state.
// but the states set by props wont be changed as getDerivedStateFromProps 
// is executed everytime just before rendering.
// But the state not set by props will be changed here the favbook gets changed
// not the favoritecolor
