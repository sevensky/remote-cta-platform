'''
Script which create instrument non nullable field

@author: julien.bernard
'''
from model.instrument import Instrument
from model.meta import Base, Session
import logging
from dao.instrument_dao import InstrumentDAO
from data_error import DataError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('InstrumentCreatorScript')

if __name__ == "__main__":
    
    
    logger.info('Starting instrument creation ...')
    
    session = Session()
    
    Base.metadata.create_all()
    
    instrument_dao = InstrumentDAO()
    
    try:
        
        ad = instrument_dao.get_by_ticker(session, 'AD')
        if not ad:
            ad = Instrument()
        ad.ticker = 'AD'
        ad.name = 'Australian Dollar'
        ad.asset_class = 'Currencies'
        ad.transactions_fees = .00005
        instrument_dao.save(session, ad)
    
        bo = instrument_dao.get_by_ticker(session, 'BO')
        if not bo:
            bo = Instrument()
        bo.ticker = 'BO'
        bo.name = 'Soybean Oil'
        bo.asset_class = 'Grains'
        bo.transactions_fees = .015
        instrument_dao.save(session, bo)

        bp = instrument_dao.get_by_ticker(session, 'BP')
        if not bp:
            bp = Instrument()
        bp.ticker = 'BP'
        bp.name = 'British Pound'
        bp.asset_class = 'Currencies'
        bp.transactions_fees = .00005
        instrument_dao.save(session, bp)
    
        c = instrument_dao.get_by_ticker(session, 'C')
        if not c:
            c = Instrument()
        c.ticker = 'C'
        c.name = 'Corn'
        c.asset_class = 'Grains'
        c.transactions_fees = 1./8.
        instrument_dao.save(session, c)
    
        cc = instrument_dao.get_by_ticker(session, 'CC')
        if not cc:
            cc = Instrument()
        cc.ticker = 'CC'
        cc.name = 'Cocoa'
        cc.asset_class = 'Softs'
        cc.transactions_fees = 1
        instrument_dao.save(session, cc)
    
        cd = instrument_dao.get_by_ticker(session, 'CD')
        if not cd:
            cd = Instrument()
        cd.ticker = 'CD'
        cd.name = 'Canadian Dollar'
        cd.asset_class = 'Currencies'
        cd.transactions_fees = .00005
        instrument_dao.save(session, cd)
    
        cl = instrument_dao.get_by_ticker(session, 'CL')
        if not cl:
            cl = Instrument()
        cl.ticker = 'CL'
        cl.name = 'Crude Oil'
        cl.asset_class = 'Energies'
        cl.transactions_fees = .01
        instrument_dao.save(session, cl)
    
        ct = instrument_dao.get_by_ticker(session, 'CT')
        if not ct:
            ct = Instrument()
        ct.ticker = 'CT'
        ct.name = 'Cotton'
        ct.asset_class = 'Softs'
        ct.transactions_fees = .05
        instrument_dao.save(session, ct)
    
        ec = instrument_dao.get_by_ticker(session, 'EC')
        if not ec:
            ec = Instrument()
        ec.ticker = 'EC'
        ec.name = 'Euro'
        ec.asset_class = 'Currencies'
        ec.transactions_fees = .00005
        instrument_dao.save(session, ec)
    
        ed = instrument_dao.get_by_ticker(session, 'ED')
        if not ed:
            ed = Instrument()
        ed.ticker = 'ED'
        ed.name = '3M Eurodollar'
        ed.asset_class = 'Financials'
        ed.transactions_fees = .0025
        instrument_dao.save(session, ed)
    
        em = instrument_dao.get_by_ticker(session, 'EM')
        if not em:
            em = Instrument()
        em.ticker = 'EM'
        em.name = '1M LIBOR'
        em.asset_class = 'Financials'
        em.transactions_fees = .005
        instrument_dao.save(session, em)
    
        fc = instrument_dao.get_by_ticker(session, 'FC')
        if not fc:
            fc = Instrument()
        fc.ticker = 'FC'
        fc.name = 'Cattle Feeder'
        fc.asset_class = 'Meats'
        fc.transactions_fees = .025
        instrument_dao.save(session, fc)
    
        gc = instrument_dao.get_by_ticker(session, 'GC')
        if not gc:
            gc = Instrument()
        gc.ticker = 'GC'
        gc.name = 'Gold'
        gc.asset_class = 'Metals'
        gc.transactions_fees = .1
        instrument_dao.save(session, gc)
    
        hg = instrument_dao.get_by_ticker(session, 'HG')
        if not hg:
            hg = Instrument()
        hg.ticker = 'HG'
        hg.name = 'Copper High Grade'
        hg.asset_class = 'Metals'
        hg.transactions_fees = .125
        instrument_dao.save(session, hg)
    
        ho = instrument_dao.get_by_ticker(session, 'HO')
        if not ho:
            ho = Instrument()
        ho.ticker = 'HO'
        ho.name = 'Heating Oil'
        ho.asset_class = 'Energies'
        ho.transactions_fees = .0005
        instrument_dao.save(session, ho)
    
        hu = instrument_dao.get_by_ticker(session, 'HU')
        if not hu:
            hu = Instrument()
        hu.ticker = 'HU'
        hu.name = 'Gasoline Reformulated Blendstock'
        hu.asset_class = 'Energies'
        hu.transactions_fees = .00075
        instrument_dao.save(session, hu)
    
        jy = instrument_dao.get_by_ticker(session, 'JY')
        if not jy:
            jy = Instrument()
        jy.ticker = 'JY'
        jy.name = 'Japanese Yen'
        jy.asset_class = 'Currencies'
        jy.transactions_fees = .00005
        instrument_dao.save(session, jy)
    
        kc = instrument_dao.get_by_ticker(session, 'KC')
        if not kc:
            kc = Instrument()
        kc.ticker = 'KC'
        kc.name = 'Coffee'
        kc.asset_class = 'Softs'
        kc.transactions_fees = .15
        instrument_dao.save(session, kc)
    
        lb = instrument_dao.get_by_ticker(session, 'LB')
        if not lb:
            lb = Instrument()
        lb.ticker = 'LB'
        lb.name = 'Lumber'
        lb.asset_class = 'Softs'
        lb.transactions_fees = 1.05
        instrument_dao.save(session, lb)
    
        lc = instrument_dao.get_by_ticker(session, 'LC')
        if not lc:
            lc = Instrument()
        lc.ticker = 'LC'
        lc.name = 'Cattle Live'
        lc.asset_class = 'Meats'
        lc.transactions_fees = .025
        instrument_dao.save(session, lc)
    
        lh = instrument_dao.get_by_ticker(session, 'LH')
        if not lh:
            lh = Instrument()
        lh.ticker = 'LH'
        lh.name = 'Hogs Lean'
        lh.asset_class = 'Meats'
        lh.transactions_fees = .025
        instrument_dao.save(session, lh)
    
        mp = instrument_dao.get_by_ticker(session, 'MP')
        if not mp:
            mp = Instrument()
        mp.ticker = 'MP'
        mp.name = 'Mexican Peso'
        mp.asset_class = 'Currencies'
        mp.transactions_fees = .0001
        instrument_dao.save(session, mp)
    
        nd = instrument_dao.get_by_ticker(session, 'ND')
        if not nd:
            nd = Instrument()
        nd.ticker = 'ND'
        nd.name = 'Nasdaq 100'
        nd.asset_class = 'Indices'
        nd.transactions_fees = .25
        instrument_dao.save(session, nd)
    
        ng = instrument_dao.get_by_ticker(session, 'NG')
        if not ng:
            ng = Instrument()
        ng.ticker = 'NG'
        ng.name = 'Natural Gas'
        ng.asset_class = 'Energies'
        ng.transactions_fees = .0005
        instrument_dao.save(session, ng)
    
        o = instrument_dao.get_by_ticker(session, 'O')
        if not o:
            o = Instrument()
        o.ticker = 'O'
        o.name = 'Oats'
        o.asset_class = 'Grains'
        o.transactions_fees = 3./4.
        instrument_dao.save(session, o)
    
        oj = instrument_dao.get_by_ticker(session, 'OJ')
        if not oj:
            oj = Instrument()
        oj.ticker = 'OJ'
        oj.name = 'Orange Juice'
        oj.asset_class = 'Softs'
        oj.transactions_fees = .1
        instrument_dao.save(session, oj)
    
        pa = instrument_dao.get_by_ticker(session, 'PA')
        if not pa:
            pa = Instrument()
        pa.ticker = 'PA'
        pa.name = 'Palladium'
        pa.asset_class = 'Metals'
        pa.transactions_fees = .375
        instrument_dao.save(session, pa)
    
        pb = instrument_dao.get_by_ticker(session, 'PB')
        if not pb:
            pb = Instrument()
        pb.ticker = 'PB'
        pb.name = 'Pork Bellies'
        pb.asset_class = 'Meats'
        pb.transactions_fees = 5.
        instrument_dao.save(session, pb)
    
        pl = instrument_dao.get_by_ticker(session, 'PL')
        if not pl:
            pl = Instrument()
        pl.ticker = 'PL'
        pl.name = 'Platinum'
        pl.asset_class = 'Metals'
        pl.transactions_fees = .15
        instrument_dao.save(session, pl)
    
        s = instrument_dao.get_by_ticker(session, 'S')
        if not s:
            s = Instrument()
        s.ticker = 'S'
        s.name = 'Soybeans'
        s.asset_class = 'Grains'
        s.transactions_fees = 1./8.
        instrument_dao.save(session, s)
    
        sb = instrument_dao.get_by_ticker(session, 'SB')
        if not sb:
            sb = Instrument()
        sb.ticker = 'SB'
        sb.name = 'Sugar #11'
        sb.asset_class = 'Softs'
        sb.transactions_fees = .01
        instrument_dao.save(session, sb)
    
        sf = instrument_dao.get_by_ticker(session, 'SF')
        if not sf:
            sf = Instrument()
        sf.ticker = 'SF'
        sf.name = 'Swiss Franc'
        sf.asset_class = 'Currencies'
        sf.transactions_fees = .0001
        instrument_dao.save(session, sf)
    
        si = instrument_dao.get_by_ticker(session, 'SI')
        if not si:
            si = Instrument()
        si.ticker = 'SI'
        si.name = 'Silver'
        si.asset_class = 'Metals'
        si.transactions_fees = .01
        instrument_dao.save(session, si)
    
        sm = instrument_dao.get_by_ticker(session, 'SM')
        if not sm:
            sm = Instrument()
        sm.ticker = 'SM'
        sm.name = 'Soybean Meal'
        sm.asset_class = 'Grains'
        sm.transactions_fees = .1
        instrument_dao.save(session, sm)
    
        sp = instrument_dao.get_by_ticker(session, 'SP')
        if not sp:
            sp = Instrument()
        sp.ticker = 'SP'
        sp.name = 'S&P 500'
        sp.asset_class = 'Indices'
        sp.transactions_fees = .25
        instrument_dao.save(session, sp)
    
        ty = instrument_dao.get_by_ticker(session, 'TY')
        if not ty:
            ty = Instrument()
        ty.ticker = 'TY'
        ty.name = 'T-Note US 10y'
        ty.asset_class = 'Financials'
        ty.transactions_fees = 1./128.
        instrument_dao.save(session, ty)
    
        us = instrument_dao.get_by_ticker(session, 'US')
        if not us:
            us = Instrument()
        us.ticker = 'US'
        us.name = 'T-Bond US'
        us.asset_class = 'Financials'
        us.transactions_fees = 1./64.
        instrument_dao.save(session, us)
    
        w = instrument_dao.get_by_ticker(session, 'W')
        if not w:
            w = Instrument()
        w.ticker = 'W'
        w.name = 'Wheat'
        w.asset_class = 'Grains'
        w.transactions_fees = 1./4.
        instrument_dao.save(session, w)
        
    except DataError, e:
        logger.error(e)
        
    logger.info('End of instrument creation')
