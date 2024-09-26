def encode_candidate_tokens(tokenizer, candidate_dict):
    candidate_tokens_dict = {}

    for k, v in candidate_dict.items():
        assert k in tokenizer.additional_special_tokens
        k_id = tokenizer.encode(k, add_special_tokens=False)[0]

        candidate_tokens_dict[k_id] = []

        can_tokens = []
        if isinstance(v, list):
            num_values = len(v)
            for c in v:
                if c in ["no comma", "string"]:
                    continue
                can_txt = str(c)

                can_txt_tokens = tokenizer.encode(can_txt, add_special_tokens=False)

                if num_values < 50:
                    can_tokens.append(can_txt_tokens)
                else:
                    can_tokens = can_tokens + can_txt_tokens

            if num_values >= 50:
                can_tokens = list(set(can_tokens))

        candidate_tokens_dict[k_id] = can_tokens

    return candidate_tokens_dict


nodule_template = {
    "num_nodule": "<|num_nodule|>",
    "nodules": [
        {
            "nodule_id": "<|nodule_id|>",
            "series": "<|series|>",
            "image": "<|image|>",
            "lobe": "<|lobe|>",
            "segment": "<|segment|>",
            "fissure": "<|fissure|>",
            "pleural": "<|pleural|>",
            "tracheobronchial": "<|tracheobronchial|>",
            "perihilar": "<|perihilar|>",
            "lung": "<|lung|>",
            "type": "<|type|>",
            "calcification_patterns": "<|calcification_patterns|>",
            "margin": "<|margin|>",
            "shape": "<|shape|>",
            "long_axis": "<|long_axis|>",
            "short_axis": "<|short_axis|>",
            "third_axis": "<|third_axis|>",
            "average_diameter": "<|average_diameter|>",
            "part_solid_diameter": "<|part_solid_diameter|>",
            "volume": "<|volume|>",
            "mass": "<|mass|>",
            "qualitative_descriptor": "<|qualitative_descriptor|>",
            "status": "<|status|>",
            "lung_rads": "<|lung_rads|>",
            "comparison_date": "<|comparison_date|>"
        }
    ],
    "overall_lung_rads": "<|overall_lung_rads|>",
    "recommend_imaging": "<|recommend_imaging|>",
    "recommend_interval": "<|recommend_interval|>",
    "follow_up_date": "<|follow_up_date|>"
}

nodule_candidates = {
    "<|num_nodule|>": list(range(50)),
    "<|nodule_id|>": list(range(50)) + ["null"],
    "<|series|>": list(range(1000)) + ["null"],
    "<|image|>": list(range(2000)) + ["null"],
    "<|lobe|>": ["right upper lobe", "right middle lobe", "right lower lobe", "left upper lobe", "lingula",
                 "left lower lobe", "null", "string"],
    "<|segment|>": ["apical", "posterior", "anterior", "lateral", "medial",
                    "superior", "medial basal", "anterior basal", "lateral basal",
                    "posterior basal", "apico-posterior", "anteromedial basal", "inferior", "null", "string"],
    "<|fissure|>": ["right minor fissure", "right major fissure", "left major fissure", "right fissural",
                    "left fissural", "fissural", "right perifissural", "left perifissural", "perifissural",
                    "null", "string"],
    "<|pleural|>": ["subpleural", "pleural-based", "peripheral", "null", "string"],
    "<|tracheobronchial|>": ["airway", "tracheal", "endotracheal", "endobronchial", "peribronchial", "peribronchovascular", "bronchovascular", "bronchocentric", "null", "string"],
    "<|perihilar|>": ["perihilar", "null", "string"],
    "<|lung|>": ["left", "right", "bilateral", "null", "string"],
    "<|type|>": ["solid", "part-solid", "mixed attenuation", "cystic", "ground glass", "hazy", "nonsolid",
                 "fluid/water", "fat", "calcified", "part-calcified", "noncalcified", "cavitary", "null", "string"],
    "<|calcification_patterns|>": ["diffuse", "central", "lamellated", "popcorn", "eccentric", "dense", "dendriform", "punctate", "linear", "null", "string"],
    "<|margin|>": ["spiculated", "smooth", "lobulated", "fuzzy", "irregular", "null", "string"],
    "<|shape|>": ["oval", "lentiform", "triangular", "round", "bilobed", "rectangular", "polygonal", "spherical",
                  "irregular", "ovoid", "tubular", "branching", "null", "string"],
    "<|long_axis|>": list(range(101)) + ["0.0", "null"],
    "<|short_axis|>": list(range(101)) + ["0.0", "null"],
    "<|third_axis|>": list(range(101)) + ["0.0", "null"],
    "<|average_diameter|>": list(range(101)) + ["0.0", "null"],
    "<|part_solid_diameter|>": list(range(101)) + ["0.0", "null"],
    "<|volume|>": list(range(10000)) + ["0.0", "null"],
    "<|qualitative_descriptor|>": ["large", "small", "tiny", "micronodule", "punctate", "scattered micronodules",
                                   "subcentimeter", "null", "string"],
    "<|mass|>": list(range(10000)) + ["0.0", "null"],
    "<|status|>": ["stable", "increase", "decrease", "new", "changed", "baseline", "interval development", "resolved",
                   "null", "string"],
    "<|lung_rads|>": ["0", "1", "2", "3", "4A", "4B", "4X", "null", "string"],
    "<|comparison_date|>": ["{:02}/01/2024".format(i) for i in range(1, 13)] +
                           ["01/{:02}/2024".format(i) for i in range(1, 32)] +
                           ["01/01/{:04}".format(i) for i in range(2000, 2026)] +
                           ["null", "string"],
    "<|overall_lung_rads|>": ["0", "1", "2", "3", "4A", "4B", "4X", "null", "string", "no comma"],
    "<|recommend_imaging|>": ["LDCT",
                              "LDCT, PET/CT",
                              "LDCT, Tissue sampling",
                              "LDCT, PET/CT, Tissue sampling",
                              "LDCT, Diagnostic CT",
                              "LDCT, Diagnostic CT, PET/CT",
                              "LDCT, Diagnostic CT, PET/CT, Tissue sampling",
                              "Diagnostic CT",
                              "Diagnostic CT with contrast",
                              "Diagnostic CT, PET/CT",
                              "Diagnostic CT with contrast, PET/CT",
                              "Diagnostic CT, PET/CT, Tissue sampling",
                              "Diagnostic CT with contrast, PET/CT, Tissue sampling",
                              "PET/CT",
                              "PET/CT, Tissue sampling",
                              "Tissue sampling",
                              "null", "string"
                              ],
    "<|recommend_interval|>": ["1 month",
                               "1-2 months",
                               "1-3 months",
                               "2-3 months",
                               "3 months",
                               "3-6 months",
                               "4-6 months",
                               "6 months",
                               "6-12 months",
                               "12 months",
                               "null", "string",
                               ],
    "<|follow_up_date|>": ["{:02}/01/2024".format(i) for i in range(1, 13)] +
                          ["01/{:02}/2024".format(i) for i in range(1, 32)] +
                          ["01/01/{:04}".format(i) for i in range(2000, 2026)] +
                          ["null", "string", "no comma"],
}

nodule_type_dict = {
    "num_nodule": "int",
    "nodule_id": "int",
    "series": "int",
    "image": "int",
    "lobe": "string",
    "segment": "string",
    "fissure": "string",
    "pleural": "string",
    "tracheobronchial": "string",
    "perihilar": "string",
    "lung": "string",
    "type": "string",
    "calcification_patterns": "string",
    "margin": "string",
    "shape": "string",
    "long_axis": "float",
    "short_axis": "float",
    "third_axis": "float",
    "average_diameter": "float",
    "part_solid_diameter": "float",
    "volume": "float",
    "mass": "float",
    "qualitative_descriptor": "string",
    "status": "string",
    "lung_rads": "string",
    "comparison_date": "string",
    "overall_lung_rads": "string",
    "management_recommendations": "string",
    "recommend_imaging": "string",
    "recommend_interval": "string",
    "follow_up_date": "string",
}

nodule_score_dict = {
    "num_nodule": 0,
    "nodule_id": 141,
    "series": 70,
    "image": 70,
    "lobe": 10,
    "segment": 10,
    "fissure": 10,
    "pleural": 10,
    "tracheobronchial": 10,
    "perihilar": 10,
    "lung": 10,
    "type": 1,
    "calcification_patterns": 1,
    "margin": 1,
    "shape": 1,
    "long_axis": 1,
    "short_axis": 1,
    "third_axis": 1,
    "average_diameter": 1,
    "part_solid_diameter": 1,
    "volume": 1,
    "mass": 1,
    "qualitative_descriptor": 1,
    "status": 1,
    "lung_rads": 1,
    "comparison_date": 1,
    "overall_lung_rads": 0,
    "management_recommendations": 0,
    "recommend_imaging": 0,
    "recommend_interval": 0,
    "follow_up_date": 0,
}
