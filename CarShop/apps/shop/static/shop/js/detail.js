function IncorrectTireSeasonException(incorrectSeasonName) {
    var message = `${incorrectSeasonName} is incorrect tire season`

    var error = Error.call(this, message);

    error.name = this.name = this.constructor.name;

    this.message = error.message;
    this.stack = error.stack;
}

IncorrectTireSeasonException.prototype = Object.create(Error.prototype, {
    constructor: { value: IncorrectTireSeasonException }
});



class Detail {
    #name;
    #price;

    constructor(name, price) {
        this.name = name;
        this.price = price;
    }

    get name() {
        return this.#name;
    }

    set name(value) {
        this.#name = value;
    }


    get price() {
        return this.#price;
    }

    set price(value) {
        if (value >= 0) {
            this.#price = value;
        } else {
            throw {
                name: 'NegativePriceException',
                __proto__: new Error('Price must be positive')
            }
        }
    }

    toString() {
        return `Detail { Name: ${this.name}, Price: ${this.price} }`
    }
}

class Tire extends Detail {
    #season;

    constructor(name, price, season) {
        super(name, price);

        this.season = season;
    }

    get season() {
        return this.#season;
    }

    set season(value) {
        value = value.trim().toLowerCase()

        if (['winter', 'summer'].includes(value)) {
            this.#season = value;
        } else {
            throw new IncorrectTireSeasonException(value);
        }
    }

    toString() {
        return `Tire { Name: ${this.name}, Price: ${this.price}, Season: ${this.season} }`
    }
}

//details
const button = document.getElementById("details")
button.addEventListener("click", function() {
    var d1 = new Detail("Gear", 10)

    alert(d1.toString())

    d1.price = 12

    alert("after change price: " + d1.toString())


    var t1 = new Tire("SuperTire", 23, 'winter')

    alert(t1)

    try {
        t1.season = 'fall'
    } catch (e) {
        if (e instanceof IncorrectTireSeasonException) {
            alert(e.message)
        } else {
            throw e;
        }
    }

});



