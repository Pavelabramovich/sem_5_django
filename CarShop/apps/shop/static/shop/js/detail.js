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


function argsToLower(func) {
    function wrapped(...args) {
        for (var i = 0; i < args.length; i++) {
            try {
                args[i] = args[i].trim().toLowerCase()
            } catch(e) {
                if (!e instanceof TypeError) {
                    throw e
                }
            }
        }

        func.call(this, ...args)
    }

    return wrapped
}

Object.defineProperty(String.prototype, 'capitalize', {
    value: function() {
        return this.charAt(0).toUpperCase() + this.slice(1);
    },
    enumerable: false
});

function retCapitalize(func) {
    function wrapped(...args) {
        try {
            return func.call(this, ...args).capitalize()
        } catch(e) {
            if (!e instanceof TypeError) {
                throw e
            }
        }
    }

    return wrapped
}




function decorateProperty(prototype, property, accessor, decorator) {
    if (!['get', 'set'].includes(accessor.trim().toLowerCase())) {
        throw new Error("Invalid accessor ot overwrite")
    }

    Object.defineProperty(prototype, property, {
        [accessor]: decorator(Object.getOwnPropertyDescriptor(prototype, property)[accessor])
    });
}




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

decorateProperty(Tire.prototype, "season", 'get', retCapitalize)
decorateProperty(Tire.prototype, "season", 'set', argsToLower)


//details
const button = document.getElementById("details")


button.addEventListener("click", function() {
    var d1 = new Detail("Gear", 10)

    alert(d1.toString())

    d1.price = 12

    alert("after change price: " + d1.toString())


    var t1 = new Tire("SuperTire", 23, 'Winter')

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



