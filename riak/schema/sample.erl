%% Schema for 'snp'

{
    schema, 
    [
        {version, "1.1"},
        {n_val, 1},
	   	{default_field, "sample_type"},
        {analyzer_factory, {erlang, text_analyzers, whitespace_analyzer_factory}}
    ],
    [
        {field, [
            {name, "sample_id"},
            {type, string},
            {analyzer_factory, {erlang, text_analyzers, noop_analyzer_factory}}
        ]},

        {field, [
            {name, "donor_id"},
            {type, string},
            {analyzer_factory, {erlang, text_analyzers, noop_analyzer_factory}}
        ]},

        {field, [
            {name, "sample_type"},
            {type, string},
            {analyzer_factory, {erlang, text_analyzers, standard_analyzer_factory}}
        ]},

        {field, [
            {name, "mutation_type"},
            {type, string},
            {analyzer_factory, {erlang, text_analyzers, standard_analyzer_factory}}
        ]},

        {field, [
            {name, "vital_status"},
            {type, string},
            {analyzer_factory, {erlang, text_analyzers, noop_analyzer_factory}}
        ]},
        {dynamic_field, [
            {name, "*"},
            {skip, true}
        ]}
    ]
}.

