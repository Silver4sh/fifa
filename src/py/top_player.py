def get_top10_players(data):
    top10_att = data.loc[
        data['Position'].isin(['CF', 'SS', 'LW', 'RW', 'ST', 'FW'])
    ].sort_values('Overall', ascending=False).head(10)
    
    top10_mid = data.loc[
        data['Position'].str.contains('M', na=False)
    ].sort_values('Overall', ascending=False).head(10)
    
    deff = data.loc[
        (data['Position'].str.contains('B', na=False)) | (data['Position'] == 'SW')
    ].sort_values('Overall', ascending=False)
    
    top10_deff = deff.head(10)
    
    top10_l_deff = deff.loc[
        deff['Position'].str.contains('L', na=False)
    ].sort_values('Overall', ascending=False).head(10)
    
    top10_c_deff = deff.loc[
        deff['Position'].str.contains('C', na=False)
    ].sort_values('Overall', ascending=False).head(10)
    
    top10_r_deff = deff.loc[
        deff['Position'].str.contains('R', na=False)
    ].sort_values('Overall', ascending=False).head(10)
    
    top10_gk = data.loc[
        data['Position'] == 'GK'
    ].sort_values(['GK', 'Overall'], ascending=False).head(10)
    
    return {
        'top10_attackers': top10_att,
        'top10_midfielders': top10_mid,
        'top10_defenders': top10_deff,
        'top10_left_defenders': top10_l_deff,
        'top10_center_defenders': top10_c_deff,
        'top10_right_defenders': top10_r_deff,
        'top10_goalkeepers': top10_gk
    }