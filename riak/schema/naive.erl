%% Schema for 'snp'

{
    schema, 
    [
        {version, "1.1"},
        {n_val, 1},
	   	{default_field, "sample_type"},
        {analyzer_factory, {erlang, text_analyzers}}
    ],
    [
        {dynamic_field, [
            {name, "*"},
            {analyzer_factory, {erlang, text_analyzers, noop_analyzer_factory}}
        ]}
    ]
}.

