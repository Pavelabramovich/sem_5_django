{
    'transpiler': 'npm/@babel/standalone@7.12.15/babel.min.js',
    'extensions': ['.jsx'],
    'options': {
        'plugins': ['transform-import-cssm'],
        "presets": ["react"],
        "generatorOpts": {
            "jsescOption": {
                "minimal": True
            }
        }
    },
    'mimetypes': {
        '.jsx': 'application/javascript'
    },
    'setup': ['npm/babel-plugin-transform-import-cssm@1.0.0/index.standalone.js']
}